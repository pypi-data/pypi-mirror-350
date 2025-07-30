from rpg.sequence import Sequence as Rpg_Sequence
import varpepdb.utils as utils
import rpg
import functools
import numbers
from typing import Tuple, Union


@functools.total_ordering
class SAP:
    def __init__(self, pos, ref, alt, string):
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.string = string

    def __lt__(self, other):
        return self.pos < other

    def __eq__(self, other):
        return self.pos == other

    def __repr__(self):
        return f"(pos={self.pos}, ref={self.ref}, alt={self.alt}, string={self.string})"


class Variant:

    enzyme = None

    def __init__(self, hgvs_str_list=None, AC=None):
        self.variants = []

        if hgvs_str_list is not None:
            self.parse_list(hgvs_str_list)

        self._get_cleave_position()
        self._get_flank_dist()
        self._get_enzyme_variants()
        self._get_nonenzyme_variants()

    def __len__(self):
        return len(self.variants)

    def __repr__(self):
        return repr(self.variants)

    def _sort(self):
        self.variants.sort(key=lambda x: x.pos)

    def _get_rule_attrib(self, rulelist, attrib):
        if len(rulelist) == 0:
            return []

        elif len(rulelist) == 1:
            return [getattr(rulelist[0], attrib)] + self._get_rule_attrib(rulelist[0].rules, attrib)

        elif len(rulelist) > 1:
            return [getattr(rulelist[0], attrib)] + self._get_rule_attrib(rulelist[0].rules, attrib) + \
                self._get_rule_attrib(rulelist[1:], attrib)

    def _get_cleave_position(self):
        position_list = []

        for enzyme_i in self.enzyme:
            position_list.extend(self._get_rule_attrib(enzyme_i.rules, 'pos'))

        self.position_list = set(position_list)

    def _get_flank_dist(self):
        index_list = []

        for enzyme_i in self.enzyme:
            index_list.extend(self._get_rule_attrib(enzyme_i.rules, 'index'))
        max_downstream = max(index_list)
        min_upstream = min(index_list)

        enzyme_recog_dist = max_downstream - min_upstream
        if enzyme_recog_dist == 0:
            self.downstream = 0
            self.upstream = 0

            if 1 in self.position_list:
                self.downstream = 1

            if 0 in self.position_list:
                self.upstream = -1

        elif enzyme_recog_dist > 0:
            self.downstream = enzyme_recog_dist
            self.upstream = -enzyme_recog_dist

        elif enzyme_recog_dist < 0:
            raise Exception(f"enzyme_recog_dist is {enzyme_recog_dist}!")

    def _get_enzyme_variants(self):
        AA_list = []

        for enzyme_i in self.enzyme:
            AA_list.extend(self._get_rule_attrib(enzyme_i.rules, 'amino_acid'))

        self.enzyme_AAs = set(AA_list)
        self.enzyme_variants = []

        for i in self.variants:
            if i.ref in self.enzyme_AAs or i.alt in self.enzyme_AAs:
                self.enzyme_variants.append(i)

    def _get_nonenzyme_variants(self):
        self.nonenzyme_variants = []

        for i in self.variants:
            if i.ref not in self.enzyme_AAs and i.alt not in self.enzyme_AAs:
                self.nonenzyme_variants.append(i)

    def parse_list(self, hgvs_str_list):
        for variant_one in hgvs_str_list:
            
            pos = int(variant_one[5:-3]) - 1  # Use 0 based position
            ref = utils.AA_3to1[variant_one[2:5]]
            alt = utils.AA_3to1[variant_one[-3:]]

            self.variants.append(SAP(pos, ref, alt, string=variant_one))

        self._sort()


class Peptide:
    max_length = 30
    min_length = 6

    def __init__(self, aa_string, identifier, gene, start=0, enzyme_variants=None, nonenzyme_variants=None,
                 miscleave_count=0, applied_enzymevariants=None, applied_nonenzymevariants=None):

        if isinstance(aa_string, str):
            self._seq = bytearray(aa_string, "ASCII")
        elif isinstance(aa_string, bytearray):
            self._seq = aa_string
        else:
            raise TypeError(
                "aa_string should be a string or bytearray object"
            )

        self.ori = self._seq
        self.identifier = identifier
        self.gene = gene
        self.start = start  # 0 based

        if enzyme_variants is None:
            enzyme_variants = []
        self.enzyme_variants = enzyme_variants

        if nonenzyme_variants is None:
            nonenzyme_variants = []
        self.nonenzyme_variants = nonenzyme_variants

        self.miscleave_count = miscleave_count

        if applied_enzymevariants is None:
            applied_enzymevariants = []
        self.applied_enzymevariants = applied_enzymevariants

        if applied_nonenzymevariants is None:
            applied_nonenzymevariants = []
        self.applied_nonenzymevariants = applied_nonenzymevariants

        self.n_applied_enzymevar = len(applied_enzymevariants)
        self.n_applied_nonenzymevar = len(applied_nonenzymevariants)

    def __eq__(self, other):
        # Compare only positions in protein and sequence
        return self.seq() == other.seq() and self.start == other.start and self.end == other.end and self.identifier == other.identifier

    def __contains__(self, other: SAP):
        return other.pos >= self.start and other.pos <= self.end

    def __add__(self, other: 'Peptide'):
        """Concentenate 2 Peptide objects
        """
        if self.end != other.start-1:
            raise RuntimeError('Sequences not contiguous, cannot be added.')

        if self.identifier != other.identifier:
            raise RuntimeError('Different sequence identifiers, cannot be added.')

        newenzyme_variants = self.enzyme_variants[:] + \
            [i for i in other.enzyme_variants if i not in self.enzyme_variants]

        newnonenzyme_variants = self.nonenzyme_variants + other.nonenzyme_variants

        newmiscleave_count = self.miscleave_count + other.miscleave_count + 1

        new_applied_enzymevariants = self.applied_enzymevariants[:] + \
            [i for i in other.applied_enzymevariants if i not in self.applied_enzymevariants]
        new_applied_nonenzymevariants = self.applied_nonenzymevariants + other.applied_nonenzymevariants

        newinstance = self.__class__(aa_string=self._seq+other._seq,
                                     identifier=self.identifier,
                                     gene=self.gene,
                                     start=self.start,
                                     enzyme_variants=newenzyme_variants,
                                     nonenzyme_variants=newnonenzyme_variants,
                                     miscleave_count=newmiscleave_count,
                                     applied_enzymevariants=new_applied_enzymevariants,
                                     applied_nonenzymevariants=new_applied_nonenzymevariants)
        return newinstance

    def __str__(self):
        return self.seq()
    
    def seq(self):
        return self._seq.decode("ASCII")

    def __repr__(self):
        return self.seq() + '\n' + f'Start: {self.start}' + '\n' + f'End: {self.end}'

    def __getitem__(self, index):

        if isinstance(index, numbers.Integral):
            start = index + self.start
            end = index + self.start
            newseq = chr(self._seq[index])
        else:
            start = self.start + (index.start or 0)
            end = self.start + index.stop - 1  # Slice doesn't include last element
            newseq = self._seq[index]
        # Todo: negative slice

        new_nonenzyme_variants = [i for i in self.nonenzyme_variants if i.pos in range(start, end+1)]
        new_applied_nonenzymevariants = [i for i in self.applied_nonenzymevariants if i.pos in range(start, end+1)]

        return self.__class__(aa_string=newseq,
                              identifier=self.identifier,
                              gene=self.gene,
                              start=start,
                              enzyme_variants=self.enzyme_variants[:],
                              nonenzyme_variants=new_nonenzyme_variants,
                              miscleave_count=self.miscleave_count,
                              applied_enzymevariants=self.applied_enzymevariants[:],
                              applied_nonenzymevariants=new_applied_nonenzymevariants)

    def __setitem__(self, index, value: str):
        """Set a subsequence of single letter via value parameter.

        >>> my_seq = Peptide('ACTCGACGTCG')
        >>> my_seq[0] = 'T'
        >>> my_seq
        Peptide('TCTCGACGTCG')
        """
        if isinstance(index, numbers.Integral):
            # Replacing a single letter with a new string
            self._seq[index] = ord(value)
        else:
            # Replacing a sub-sequence
            if isinstance(value, Peptide):
                self._seq[index] = value._seq
            elif isinstance(value, str):
                self._seq[index] = value.encode("ASCII")
            else:
                raise TypeError(f"received unexpected type '{type(value).__name__}'")

    def __len__(self):
        return len(self._seq)

    @property
    def start(self):
        """Setting the start position automatically sets the end
        """
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        self._end = value + len(self._seq) - 1

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        raise AttributeError('End position is read-only. Set the start position only. ')

    def apply_tuple_combination(self, one_combination: Tuple[int, str, Union[None, SAP]], variant_type: str):
        """Apply one amino acid substitution

        Args:
            one_combination: A tuple describing the amino acid substition.
                May also substitute back to canonical sequence.
            variant_type: enzyme or nonenzyme
        """

        if variant_type not in ['enzyme', 'nonenzyme']:
            raise ValueError('variant_type must be enzyme or nonenzyme')

        for one_change in one_combination:
            skip_current_change = False
            sap_string = one_change[2].string if one_change[2] else f"ref {one_change[1]} at pos {one_change[0]}"

            for i in self.applied_nonenzymevariants:
                if one_change[0] == i.pos:
                    raise RuntimeError(f'{self.identifier}: {i.string} already applied. \
                                    Applying {sap_string} overwrites it.')

            for i in self.applied_enzymevariants:
                if one_change[0] == i.pos:
                    print(f'{self.identifier}: {i.string} enzyme variant already applied. Ignoring {sap_string}. ')
                    skip_current_change = True

            if skip_current_change:
                continue

            index = one_change[0]-self.start  # Convert global position to local position
            target = one_change[1]

            self[index] = target

            if one_change[2]:  # If there is a SAP object
                if variant_type == 'enzyme':
                    self.applied_enzymevariants.append(one_change[2])
                    self.n_applied_enzymevar += 1

                elif variant_type == 'nonenzyme':
                    self.applied_nonenzymevariants.append(one_change[2])
                    self.n_applied_nonenzymevar += 1

    def add_enzyme_variants(self, v):
        self.check_variant(v)
        self.enzyme_variants.append(v)

    def add_nonenzyme_variants(self, v):
        self.check_variant(v)
        self.nonenzyme_variants.append(v)

    def check_variant(self, v):
        if str(self[v.pos-self.start]) != v.ref:
            raise RuntimeError(f'Reference amino acid is wrong in {v.string} for {self.identifier}.')

    def convert_rpg(self):
        return Rpg_Sequence(self.identifier, str(self))

    def restore_original(self):
        self._seq = self.ori
        self.applied_nonenzymevariants = []

    def within_length(self):
        return len(self) >= self.min_length and len(self) <= self.max_length

    def not_too_long(self):
        return len(self) <= self.max_length


class Cleaver:
    """Cleave peptide object with enzyme

    Returns:
       List of cleaved peptides. Cleaved peptides that exceed length limit are excluded.
    """
    enzyme = None

    def __init__(self, aa_pka=rpg.core.AA_PKA_IPC, aa_mass=rpg.core.AA_MASS_AVERAGE, water_mass=rpg.core.WATER_MASS):

        self.aa_pka = aa_pka
        self.water_mass = water_mass
        self.aa_mass = aa_mass

    def __call__(self, aaseq: 'Peptide'):

        cleave_result = self.cleave(aaseq)
        cleave_positions = [0] + [int(i) for i in cleave_result.get_cleavage_pos().split(',') if i] + [len(aaseq)]
        cleaved_peptides_list = []

        for ind in range(len(cleave_positions)-1):
            cleaved_peptide = aaseq[cleave_positions[ind]:cleave_positions[ind+1]]

            if cleaved_peptide.not_too_long():
                cleaved_peptide.miscleave_count = 0
                cleaved_peptides_list.append(cleaved_peptide)
            else:
                continue

        return cleaved_peptides_list

    def __repr__(self):
        return f"Cleaver object with Enzyme(s) = {', '.join([i.name for i in Cleaver.enzyme])}"

    def cleave(self, aaseq: 'Peptide'):
        cleave_result = rpg.digest.digest_one_sequence(seq=aaseq.convert_rpg(),
                                                       enz=Cleaver.enzyme,
                                                       mode='concurrent',
                                                       aa_pka=self.aa_pka,
                                                       aa_mass=self.aa_mass,
                                                       water_mass=self.water_mass)[0]
        return cleave_result
