import itertools
import copy
import varpepdb.classes as vc
import varpepdb.utils as utils
from collections import Counter
import re
import multiprocessing as mp
from typing import List, Tuple, Union

miscleave = True
discardcanonical = True
cleaver = vc.Cleaver()
createcombi = True  # To create combinations of SAPs or not
message = True


def generate(input_list: List[Tuple[List[str], str, str, str]], proc: int = mp.cpu_count()) -> \
    List[vc.Peptide]:
    """Generates variant peptides with parallel processing

    Performs a check on the input list and then evokes ``generate_single`` for each input in parallel.

    Args:
        input_list: List of input. Each input element is a list consisting of the following 3 elements.                    
                    1. An list of HGVS nomenclatures describing amino acid substitution.
                        eg ['p.Gly1197Arg', 'p.Thr988Met',...]
                    2. Sequence of amino acid for the protein
                        'MTRSPPLRELPPSYTPPARTAAPQILAGSLKAPL...'
                    3. Gene name of the protein.
                        eg 'PTCH2'
                    4. Identifier for the protein
                        eg Uniprot accension number
        proc: Number of processes to run in parallel for each input.
                    Defaults to the number of cores available

    Raises:
        ValueError: If there are errors in the list of HGVS nomenclatures

    Returns:
        List of all variant peptides containing different combinations of the single amino acid substitutions.
    """

    # Check all inputs and show all errors
    error_list = []
    for idx in range(len(input_list)):

        hgvs_str_list = input_list[idx][0]

        correct_count = sum([bool(re.match(r'^p\.[A-Z][a-z]{2}\d+[A-Z][a-z]{2}', i)) for i in hgvs_str_list])
        if correct_count != len(hgvs_str_list):
            error_list.append(f'Element {idx} of input: One or more entries of variant list \
                              do not obey HGVS nomenclature.')
            
        if len(hgvs_str_list) == 0:
            if message:
                print('Variant list is empty. Generating only canonical peptides.')

        elif max(Counter(hgvs_str_list).values()) > 1:

            duplicated_list = []
            for item in Counter(hgvs_str_list).items():
                if item[1] > 1:
                    duplicated_list.append(item[0])

            error_list.append(f'Element {idx} of input: {", ".join(duplicated_list)} duplicated in variant list')

    if len(error_list) > 0:
        raise ValueError('\n'.join(error_list))

    # Run parallel processes
    with mp.Pool(proc) as pool:

        res = pool.starmap(generate_single, input_list)

    flatten_res = [j for i in res for j in i]

    return flatten_res


def generate_single(variants: List[str], sequence: str, gene: str, identifier: str) -> List[vc.Peptide]:
    """Generates variant peptides for one input.

    Args:
        variants: An list of HGVS nomenclatures describing amino acid substitution. eg. ['p.Gly1197Arg', ...]
        AA_wt_str: Sequence of amino acid for the protein.
        gene: Gene name of the protein. This is included as part of the description in the fasta header.

    Returns:
        List of all variant peptides containing different combinations of single amino acid substitutions.
    """
    # TODO: Include checking function    
    variants = vc.Variant(variants)
    peptide = vc.Peptide(sequence, identifier, gene)

    # Generate breaker peptides
    peptide_list = _generate_breaker_peptides(variants, peptide)

    cleaved_within_list = []
    cleaved_within_vars = []
    miscleaved_within_vars = []

    for peptide in peptide_list:

        peptide = _allocate_variants_to_peptide(variants, peptide)

        # List of peptides cleaved within breakers that are not too long
        cleaved_within = _cleave_breaker_peptides(peptide)

        # Select cleaved AA_sequence based on shortest variant list.
        # For peptides with more than 1 shortest variant list, add up the list.
        # Such peptides can be generated with more than 1 combination.
        cleaved_within_flat = [j for i in cleaved_within for j in i]
        cleaved_list = _deduplicate(cleaved_within_flat)
        cleaved_within_list.append(cleaved_list)

        # Sprinkle variants to cleaved peptides
        for cleaved_peptide in cleaved_list:

            cleaved_variant = _sprinkle_variants(peptide=cleaved_peptide)
            cleaved_within_vars.extend(cleaved_variant)

        if miscleave:

            # Miscleavaging within breakers
            miscl_pep_within = _miscleave_within_breakers(cleaved_within)
            miscleaved_list = _deduplicate(miscl_pep_within)

            # Sprinkle variants to peptides miscleaved within breakers
            for miscleaved_peptide in miscleaved_list:

                miscleaved_variant = _sprinkle_variants(peptide=miscleaved_peptide)
                miscleaved_within_vars.extend(miscleaved_variant)

    # Miscleavaging between breakers
    miscleaved_bet_vars = []
    if miscleave:

        for i in range(len(cleaved_within_list)-1):
            curr_list = cleaved_within_list[i]
            next_list = cleaved_within_list[i+1]

            if len(curr_list) == 0 or len(next_list) == 0:
                continue

            miscl_pep_bet = _miscleave_bet_breakers(curr_list, next_list)

            for pep in miscl_pep_bet:
                miscleaved_variant = _sprinkle_variants(peptide=pep)
                miscleaved_bet_vars.extend(miscleaved_variant)
    if message:
        print(f'completed {identifier}')

    return cleaved_within_vars + miscleaved_within_vars + miscleaved_bet_vars


def variant_containing_peptides(peptide_list: List[vc.Peptide]) -> List[vc.Peptide]:
    """Removes variant peptides that do not contain at least 1 amino acid substitution

    A segment of a protein may contain only a single amino acid substitution that causes enzymatic cleavage.
    One of the resulting peptides is a variant peptide that may not contain any amino acid substitution.
    For example, a p.Gly11Arg substitution in this protein FNGIYADPSGHNGYDA will result in FNGIYADPSR
    and HNGYDA after digestion by trypsin. HNGYDA is a variant peptide as it cannot be found by digesting
    the canonical sequence, but it doesn't contain any amino acid substitution within itself.

    This function removes such variant peptides that don't contain amino acid substitution.

    Args:
        peptide_list

    Returns:
        List of peptides containing at least 1 amino acid substitutions
    """

    informative_peptides = []

    for one_peptide in peptide_list:

        peptide_posrange = range(one_peptide.start, one_peptide.end + 1)
        allvariants = one_peptide.applied_nonenzymevariants + one_peptide.applied_enzymevariants

        # Keep canonical variants
        if not discardcanonical and len(allvariants) == 0:
            informative_peptides.append(one_peptide)
            continue

        for variant in allvariants:
            if variant.pos in peptide_posrange:

                informative_peptides.append(one_peptide)
                break

    return informative_peptides


def write(write_path: str, peptides: List[vc.Peptide], include_non_unique: bool = True) -> None:
    """Writes variant peptides into fasta file

    Example of an entry written into fasta file:
    >A0A8I5KQE6-v1.1 RPSA2 129-143 (p.Pro143Arg),p.Thr135Met 0
    ADHQPLMEASYVNLR

    'A0A8I5KQE6' is the sequence identifier of the parent protein (in this case the Uniprot ascension number) with
    'v1.1' is variant 1 of this peptide. 'v1.0' is the canonical peptide.    
    'RPSA2' is the name of the gene for this protein.
    '129-143' is the position of the parent protein sequence from which this peptide is dervied.
    '(p.Pro143Arg)' is an amino acid substitution that affected the enzyme cleavage site. Amino acid substitutions that
    introduce or remove cleavage sites are marked by parenthesis.
    'p.Thr135Met' is an amino acid subtstitution that didn't affect enzyne cleavage site.
    '0' refers to the number of miscleavages

    Args:
        write_path: Path of fasta file output
        peptide_list: List of variant peptide objects
        include_non_unique: Include variant peptides with non-unique sequences. Defaults to True. Identifier and
        description in the headers from each non-unique sequence are concatenated with a '/' as separator.

    Returns:
        None
    """

    unique_peptides, nonunique_peptides = separate_nonunique(peptides)

    unique_peptides.sort(key=lambda x: (x.identifier, x.start))

    fh = open(write_path, "w")

    v_group_counter = 0
    for _, peptide_group in itertools.groupby(unique_peptides, key=lambda x: (x.identifier, x.start, x.end)):

        v_counter = 0
        v_group_counter += 1

        for peptide in peptide_group:

            n_applied_enzymes = peptide.n_applied_enzymevar + peptide.n_applied_nonenzymevar

            # If canonical, use 0
            if n_applied_enzymes == 0:                        
                v_counter_actual = 0
            else:
                v_counter += 1
                v_counter_actual = v_counter
            identifier = peptide.identifier + '-v' + str(v_group_counter) + '.' + str(v_counter_actual)
            description = _make_description(peptide)

            # seqrecord = SeqRecord(Seq(str(peptide)),
            #                       id=identifier,
            #                       name=identifier,
            #                       description=description)

            utils.write_fasta(str(peptide), identifier, description, fh)

    if include_non_unique:

        name_tracker = Counter()

        for nonunique_list in nonunique_peptides:

            combined_identifier = '/'.join([i.identifier for i in nonunique_list])
            combined_description = '/'.join([_make_description(i) for i in nonunique_list])

            v_no = name_tracker[combined_identifier] + 1
            appended_identifier = combined_identifier + f'-v{v_no}'

            utils.write_fasta(str(nonunique_list[0]), appended_identifier, combined_description, fh)

            name_tracker[combined_identifier] += 1

    fh.close()


def separate_nonunique(peptide_list: List[vc.Peptide]) -> Tuple[List[vc.Peptide], List[List[vc.Peptide]]]:
    """Identifies variant peptide with unique and non-unique sequences

    Args:
        peptide_list: List of variant peptide objects.

    Returns:
        Tuple of 2. First element is a list of variant peptide with unique sequences. Second element is
        list of list of variant peptides sharing the same non-unique sequences.
    """
    peptide_list.sort(key=str)

    unique_seq = []
    duplicated_seq = []

    for _, peptide in itertools.groupby(peptide_list, key=str):
        pep_list = list(peptide)

        if len(pep_list) == 1:
            unique_seq.append(pep_list[0])

        else:
            duplicated_seq.append(pep_list)

    return unique_seq, duplicated_seq


def _get_tuple_combinations(variants: List[vc.SAP], omit: List[vc.SAP] = None) \
    -> List[Tuple[Tuple[int, str, Union[None, vc.SAP]]]]:
    """Creates all combinations of amino acid substitutions from a list of variants

    Args:
        variants: Variant object
        omit: Variants sharing the same positions found in this list are ignored.
        Defaults to None.

    Returns:
        List of tuples. Each tuple is a combination of amino acid substitutions to generate
        one variant peptide. An amino acid substitution is itself represented by a tuple. First element is position for
        substitution, second element is the amino acid to substitute in, third element is
        the variant object or ``None`` if this combination substitutes in the canonical amino
        acid.
    """

    if omit is None:
        omit = []
    enzyme_variant_pos = [i.pos for i in omit]
    variants[:] = [i for i in variants if i.pos not in enzyme_variant_pos]
    variants.sort(key=lambda x: x.pos)

    allpos_tuple_list = []

    for pos, sap in itertools.groupby(variants, key=lambda x: x.pos):
        sap_list = list(sap)
        onepos_tuple_list = []  # (position, AA to change to, SAP object)        
        if createcombi:
            # Add in reference amino acid
            onepos_tuple_list.append((pos, sap_list[0].ref, None))
        for sap_i in sap_list:
            onepos_tuple_list.append((pos, sap_i.alt, sap_i))
        allpos_tuple_list.append(onepos_tuple_list)
    tuple_combinations = list(itertools.product(*allpos_tuple_list))

    return tuple_combinations


def _allocate_variants_to_peptide(variants: vc.Variant, peptide: vc.Peptide) -> vc.Peptide:

    peptide = copy.deepcopy(peptide)
    for vartype in ('enzyme', 'nonenzyme'):
        for variant_i in getattr(variants, f'{vartype}_variants'):
            if variant_i in peptide:
                getattr(peptide, f'add_{vartype}_variants')(variant_i)

    return peptide


def _sprinkle_variants(peptide: vc.Peptide) -> List[vc.Peptide]:
    """Applies different combinations of amino acid substitutions

    Creates all possible combinations of amino acid substitutions that do not affect
    enzyme cleavage sites and applies each of them to generate variant peptides.
    If discardcanonical is True, canonical sequences will be discarded.

    Args:
        peptide: Peptide object

    Returns:
       List of variant peptides
    """

    peptide_variant = []

    # Omit nonenzyme variants acting on the same positions as applied enzyme variants to prevent the following situation:
    # Variant introducing a cleavage site (i.e. enzymevariant) is applied and resulted in cleavage
    # Another variant at that same position which doesn't cause cleavage overwrites the enzyme variant
    # Ends up with a cleaved peptide that doesn't have the cleavage site
    tuplecombi = _get_tuple_combinations(peptide.nonenzyme_variants, omit=peptide.applied_enzymevariants)

    for one_combi in tuplecombi:
        peptide_cp = copy.deepcopy(peptide)
        peptide_cp.apply_tuple_combination(one_combi, 'nonenzyme')

        # Exclude peptide if it is too short
        if not peptide_cp.within_length():
            continue

        # Exclude peptide if it contains 0 variant applied
        if discardcanonical:
            if peptide_cp.n_applied_enzymevar + peptide_cp.n_applied_nonenzymevar == 0:
                continue
        peptide_variant.append(peptide_cp)

    return peptide_variant


def _deduplicate(cleaved_peptides_flatten: List[vc.Peptide]) -> List[vc.Peptide]:
    """Deduplicate cleaved peptides

    Different combinations of amino acid substitutions may produce the same peptide after
    enzymatic cleaving. This function selects for the most parsimonious combination.

    Args:
        cleaved_peptides_flatten: List of peptide after cleaving

    Returns:
        List of peptide with unique sequences and most straightforward amino acid substitutions.
    """
    cleaved_peptides_flatten_c = copy.deepcopy(cleaved_peptides_flatten)
    # Group by seq, and start/end position. Positions are needed to differentiate repeated motifs.
    cleaved_peptides_flatten_c.sort(key=lambda x:(str(x), x.start, x.end))    
    group_iter = itertools.groupby(cleaved_peptides_flatten_c, key= lambda x:(str(x), x.start, x.end))

    dedup_list = []
    for _, peptide_group in group_iter:
        peptide_list = list(peptide_group)

        min_nvariants = min([i.n_applied_enzymevar for i in peptide_list])

        min_idx_list = []
        for idx, pep in enumerate(peptide_list):
            if pep.n_applied_enzymevar == min_nvariants:
                min_idx_list.append(idx)

        firstpeptide = peptide_list[min_idx_list[0]]

        # If there is more than 1 combination of enzymatic SAPs leading to the same cleaved peptide, just use the first combination found
        # and print a warning
        if len(min_idx_list) > 1:
            if message:
                print('Warning: More than 1 combination of enymatic SAPs producing the same peptide found')

        dedup_list.append(firstpeptide)

    return dedup_list


def _miscleave_within_breakers(cleaved_within: List[List[vc.Peptide]]) -> List[vc.Peptide]:

    miscleaved_peptide_list = []
    # one_combi_cleaved is list of cleaved peptides after applying 1 tuple combination
    for one_combi_cleaved in cleaved_within:
        # Apply miscleavages within each one_combi_cleaved
        for i in range(len(one_combi_cleaved)-1):
            if one_combi_cleaved[i+1].start - one_combi_cleaved[i].end == 1:

                miscleaved_peptide = one_combi_cleaved[i] + one_combi_cleaved[i+1]

                if miscleaved_peptide.within_length():
                    miscleaved_peptide_list.append(miscleaved_peptide)

            elif one_combi_cleaved[i+1].start - one_combi_cleaved[i].end - 1 <= vc.Peptide.max_length:
                raise RuntimeError(f'Peptide within length limits missing in generating miscleaved peptides for \
                                   {one_combi_cleaved[i].identifier}')

            else:
                # Contiguous peptide was longer than limit and removed. Miscleave peptide would have been too long.
                pass

    return miscleaved_peptide_list


def _cleave_breaker_peptides(peptide: vc.Peptide) -> List[vc.Peptide]:

    # Generate tuple combinations
    tuple_combinations = _get_tuple_combinations(peptide.enzyme_variants)

    # Generate cleaved AA_Sequence for all combinations of enzyme SAPs within breakers

    if len(tuple_combinations) == 0:
        cleave_result = cleaver.cleave(peptide)

        if cleave_result.nb_cleavage > 0:
            raise RuntimeError('Cleavage occurred within breaker without enzyme variants!')

        if peptide.not_too_long():  # Keep peptides for miscleavaging later
            peptide.miscleave_count = 0
            cleaved_peptides = [peptide]
        else:
            cleaved_peptides = []

    else:
        # Apply variants and cleave
        cleaved_peptides = []
        for tuple_combinations_i in tuple_combinations:
            peptide_cp = copy.deepcopy(peptide)
            peptide_cp.apply_tuple_combination(tuple_combinations_i, variant_type='enzyme')
            applied_cleaved = cleaver(peptide_cp)
            if not createcombi:
                # If not creating combi, replace certain peptides with canonical peptides
                # To account for certain edge cases like
                # SEGGTAQLLRR with a subsitution at the C terminus. 
                # SEGGTAQLLR could be generated canonically without any enzyme-SAP
                # So should be considered as canonical
                non_applied_cleaved = cleaver(peptide)
                for i in range(len(applied_cleaved)):
                    for j in non_applied_cleaved:
                        if applied_cleaved[i] == j:
                            applied_cleaved[i] = j
                            
            cleaved_peptides.append(applied_cleaved)

    return cleaved_peptides


def _generate_breaker_peptides(variants: vc.Variant, peptide: vc.Peptide) -> List[vc.Peptide]:

    WT_cleave_result = cleaver.cleave(peptide)
    positions_to_remove = []

    for enzyme_variant in variants.enzyme_variants:
        positions_to_remove.extend(range(enzyme_variant.pos + variants.upstream,
                                         enzyme_variant.pos + variants.downstream + 1))

    cleave_pos_str = WT_cleave_result.get_cleavage_pos()

    if len(cleave_pos_str) > 0:
        cleave_pos = set([int(i) for i in WT_cleave_result.get_cleavage_pos().split(',')])
    else:  # No endogenous cleave sites
        cleave_pos = set()

    cleave_pos_leftover = [0] + sorted(list(cleave_pos.difference(positions_to_remove))) + [len(peptide)]

    peptide_list = []
    for ind in range(len(cleave_pos_leftover)-1):
        peptide_list.append(peptide[cleave_pos_leftover[ind]:cleave_pos_leftover[ind+1]])
    return peptide_list


def _miscleave_bet_breakers(curr_list: List[vc.Peptide], next_list: List[vc.Peptide]) -> List[vc.Peptide]:

    miscleaved_bet = []

    curr_end_pos = max([i.end for i in curr_list])
    next_start_pos = min([i.start for i in next_list])

    if next_start_pos == curr_end_pos + 1:

        curr_idx = []
        for idx, peptide in enumerate(curr_list):
            if peptide.end == curr_end_pos:
                curr_idx.append(idx)

        next_idx = []
        for idx, peptide in enumerate(next_list):
            if peptide.start == next_start_pos:
                next_idx.append(idx)

        for i, j in itertools.product(curr_idx, next_idx):

            miscleaved_peptide = curr_list[i] + next_list[j]

            if miscleaved_peptide.within_length():
                miscleaved_bet.append(miscleaved_peptide)

    return miscleaved_bet


def _make_description(peptide: vc.Peptide) -> str:
    """Makes description for fasta entry header

    Args:
        peptide: Variant peptide object

    Raises:
        RuntimeError: If peptide doesn't arise from an amino acid substitution and can be
        obtained from the canonical sequence

    Returns:
        Description for fasta entry header
    """

    enzymevar = ','.join([i.string for i in peptide.applied_enzymevariants])
    nonenzymevar = ','.join([i.string for i in peptide.applied_nonenzymevariants])

    if peptide.applied_enzymevariants and peptide.applied_nonenzymevariants:
        variant_string = '(' + enzymevar + '),' + nonenzymevar

    elif peptide.applied_enzymevariants and not peptide.applied_nonenzymevariants:
        variant_string = '(' + enzymevar + ')'

    elif not peptide.applied_enzymevariants and peptide.applied_nonenzymevariants:
        variant_string = nonenzymevar

    else:
        variant_string = 'Canonical'

    pos_range = str(peptide.start + 1) + '-' + str(peptide.end + 1)

    description = ' '.join([peptide.gene, pos_range, variant_string, str(peptide.miscleave_count)])

    return description
