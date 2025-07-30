#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for atom type assignment for oplsaa+ forcefield.

These were originally developed using the SMILES from OpenBabel.
When the default for SMILES was changed to RDKit, tests with explicit
hydrogens in the SMILES failed because RDKit produces a different order
of atoms than OpenBabel in these cases. For the time being, in these tests
the call to configuration.smiles adds the argument 'flavor="openbabel"' to continue
using OpenBabel.
"""


if True:

    def test_opls_58(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 58, Helium atom"""
        correct = ["opls_58"]
        configuration.from_smiles("[He]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_59(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 59, Neon atom"""
        correct = ["opls_59"]
        configuration.from_smiles("[Ne]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_60(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 60, Argon atom"""
        correct = ["opls_60"]
        configuration.from_smiles("[Ar]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_61(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 61, Krypton atom"""
        correct = ["opls_61"]
        configuration.from_smiles("[Kr]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_62(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 62, Xenon atom"""
        correct = ["opls_62"]
        configuration.from_smiles("[Xe]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_76(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 76,  SPC water O"""
        correct = ["opls_76", "opls_77", "opls_77"]
        configuration.from_smiles("O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_77(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 77,  SPC water H"""
        correct = ["opls_76", "opls_77", "opls_77"]
        configuration.from_smiles("O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_78_and_79(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 78,  ammonia N & H"""
        correct = ["opls_78", "opls_79", "opls_79", "opls_79"]
        configuration.from_smiles("N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_80(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 80,  alkane methyl group"""
        correct = 2 * ["opls_80"] + 6 * ["opls_85"]
        configuration.from_smiles("CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_81(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 81,  alkane methylene group"""
        correct = ["opls_81"] + 2 * ["opls_80"] + 8 * ["opls_85"]
        configuration.from_smiles("C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_82(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 82,  alkane >CH- group"""
        correct = ["opls_82"] + 3 * ["opls_80"] + 10 * ["opls_85"]
        configuration.from_smiles("C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_83(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 83,  methane carbon"""
        correct = ["opls_83"] + 4 * ["opls_85"]
        configuration.from_smiles("C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_84(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 84,  alkane >C< group"""
        correct = ["opls_84"] + 4 * ["opls_80"] + 12 * ["opls_85"]
        configuration.from_smiles("C(C)(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_86(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 86,  alkene R2C= group"""
        correct = (
            ["opls_86"]
            + 2 * ["opls_80"]
            + ["opls_88"]
            + 6 * ["opls_85"]
            + 2 * ["opls_89"]
        )
        configuration.from_smiles("C(C)(C)=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_87(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 87,  alkene RCH= group"""
        correct = (
            ["opls_87"]
            + ["opls_80"]
            + ["opls_88"]
            + ["opls_89"]
            + 3 * ["opls_85"]
            + 2 * ["opls_89"]
        )
        configuration.from_smiles("C(C)=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_88(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 88,  alkene CH2= group"""
        correct = 2 * ["opls_88"] + 4 * ["opls_89"]
        configuration.from_smiles("C=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_90(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 90,  aromatic C"""
        correct = 6 * ["opls_90"] + 6 * ["opls_91"]
        configuration.from_smiles("c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_92(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 92,  Naphthalene junction C"""
        correct = (
            3 * ["opls_90"]
            + ["opls_92"]
            + 4 * ["opls_90"]
            + ["opls_92", "opls_90"]
            + 8 * ["opls_91"]
        )
        configuration.from_smiles("C1=CC=C2C=CC=CC2=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_93(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 93,  Methyl benzene -CH3 carbon"""
        correct = ["opls_93"] + 6 * ["opls_90"] + 3 * ["opls_85"] + 5 * ["opls_91"]
        configuration.from_smiles("Cc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_94(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 94,  Methylene benzene -CH2- carbon"""
        correct = (
            ["opls_80", "opls_94"] + 6 * ["opls_90"] + 5 * ["opls_85"] + 5 * ["opls_91"]
        )
        configuration.from_smiles("CCc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_456(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 456,  Methine benzene -C2< carbon"""
        correct = (
            ["opls_456"]
            + 2 * ["opls_80"]
            + 6 * ["opls_90"]
            + 7 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("C(C)(C)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_457(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 457,
        quaternary benzene Ar-CR3 carbon
        """
        correct = (
            ["opls_457"]
            + 3 * ["opls_80"]
            + 6 * ["opls_90"]
            + 9 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("C(C)(C)(C)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_95(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 95,  diene =C-C="""
        correct = ["opls_88", "opls_95", "opls_95", "opls_88"] + 6 * ["opls_89"]
        configuration.from_smiles("C=CC=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_96(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 96, alcohol O"""
        correct = ["opls_99", "opls_96"] + 3 * ["opls_98"] + ["opls_97"]
        configuration.from_smiles("CO")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_99(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 99, R-CH2-OH carbon"""
        correct = ["opls_80", "opls_99", "opls_96"] + 5 * ["opls_85"] + ["opls_97"]
        configuration.from_smiles("CCO")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_103(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 103-107 trifluorethanol"""
        correct = (
            ["opls_103"]
            + 3 * ["opls_106"]
            + ["opls_102", "opls_104"]
            + 2 * ["opls_107"]
            + ["opls_105"]
        )
        configuration.from_smiles("C(F)(F)(F)CO")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_108(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 108-110 phenolic C-OH"""
        correct = (
            ["opls_109", "opls_108"] + 5 * ["opls_90"] + ["opls_110"] + 5 * ["opls_91"]
        )
        configuration.from_smiles("Oc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_111(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 111, 112, 115-118 diols"""
        correct = (
            ["opls_111", "opls_115", "opls_115", "opls_111"]
            + ["opls_112"]
            + 4 * ["opls_118"]
            + ["opls_112"]
        )
        configuration.from_smiles("OCCO")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_113(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 113, 114, 115-118 triols"""
        correct = (
            ["opls_115", "opls_113", "opls_114"]
            + ["opls_116", "opls_113", "opls_114"]
            + ["opls_115", "opls_113", "opls_114"]
            + 5 * ["opls_118"]
        )
        configuration.from_smiles("C(O[H])C(O[H])CO[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # test CR2OH
        correct = (
            ["opls_115", "opls_113", "opls_114"]
            + ["opls_116", "opls_113", "opls_114"]
            + ["opls_117", "opls_113", "opls_114"]
            + 2 * ["opls_80"]
            + 3 * ["opls_118"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("C(O[H])C(O[H])C(O[H])(C)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_116(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 111, 112, 116, 118 diols"""
        correct = (
            ["opls_111", "opls_115", "opls_116", "opls_80", "opls_111"]
            + ["opls_112"]
            + 3 * ["opls_118"]
            + 3 * ["opls_85"]
            + ["opls_112"]
        )
        configuration.from_smiles("OCC(C)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_117(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 111, 112, 117, 118 diols"""
        correct = (
            ["opls_111", "opls_115", "opls_117", "opls_80", "opls_80", "opls_111"]
            + ["opls_112"]
            + 2 * ["opls_118"]
            + 6 * ["opls_85"]
            + ["opls_112"]
        )
        configuration.from_smiles("OCC(C)(C)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed 116 and 117
        correct = (
            ["opls_111", "opls_116", "opls_80", "opls_117"]
            + 2 * ["opls_80"]
            + ["opls_111"]
            + ["opls_112"]
            + ["opls_118"]
            + 9 * ["opls_85"]
            + ["opls_112"]
        )
        configuration.from_smiles("OC(C)C(C)(C)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_119(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 119 diphenyl ether O"""
        correct = ["opls_119"] + 12 * ["opls_90"] + 10 * ["opls_91"]
        configuration.from_smiles("O(c1ccccc1)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_120(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 120,  diene =CR-CR="""
        correct = (
            ["opls_88", "opls_120", "opls_80", "opls_120", "opls_80", "opls_88"]
            + 2 * ["opls_89"]
            + 6 * ["opls_85"]
            + 2 * ["opls_89"]
        )
        configuration.from_smiles("C=C(C)C(C)=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed =CR-C=
        correct = (
            ["opls_88", "opls_120", "opls_80", "opls_95", "opls_88"]
            + 2 * ["opls_89"]
            + 3 * ["opls_85"]
            + 3 * ["opls_89"]
        )
        configuration.from_smiles("C=C(C)C=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_121(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 123, carbon in methyl ether;
        opls 127, hydrogens adjacent to ether oxygen
        opls 121, oxygen in anisole;
        opls 141, phenyl carbon in anisole
        """
        correct = (
            ["opls_123", "opls_121", "opls_141"]
            + 5 * ["opls_90"]
            + 3 * ["opls_127"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("COc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_122(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 122, alkyl ether oxygen;
        opls 123, methyl ether carbon;
        opls 127, alkyl ether hydrogen
        """
        correct = ["opls_122", "opls_123", "opls_123"] + 6 * ["opls_127"]
        configuration.from_smiles("O(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_124(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 122, alkyl ether oxygen;
        opls 124, secondary ether carbon;
        opls 127, alkyl ether hydrogen
        """
        correct = (
            ["opls_122", "opls_124", "opls_80", "opls_124", "opls_80"]
            + 2 * ["opls_127"]
            + 3 * ["opls_85"]
            + 2 * ["opls_127"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("O(CC)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed: methylethyl ether
        correct = (
            ["opls_122", "opls_124", "opls_80", "opls_123"]
            + 2 * ["opls_127"]
            + 3 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("O(CC)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_125(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 122, alkyl ether oxygen;
        opls 125, tertiary ether carbon;
        opls 127, alkyl ether hydrogen
        """
        correct = (
            ["opls_122"]
            + 2 * ["opls_125", "opls_80", "opls_80"]
            + ["opls_127"]
            + 6 * ["opls_85"]
            + ["opls_127"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("O(C(C)C)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed: methylisopropyl ether
        correct = (
            ["opls_122"]
            + ["opls_125", "opls_80", "opls_80"]
            + ["opls_123"]
            + ["opls_127"]
            + 6 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("O(C(C)C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_126(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 122, alkyl ether oxygen;
        opls 126, quaternary ether carbon;
        opls 127, alkyl ether hydrogen
        """
        correct = (
            ["opls_122"]
            + 2 * ["opls_126", "opls_80", "opls_80", "opls_80"]
            + 18 * ["opls_85"]
        )
        configuration.from_smiles("O(C(C)(C)C)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed: methyltbutyl ether
        correct = (
            ["opls_122"]
            + ["opls_126", "opls_80", "opls_80", "opls_80"]
            + ["opls_123"]
            + 9 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("O(C(C)(C)C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_128(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 131, acetal methylene carbon;
        opls 132, hydrogen on acetal methylene carbon
        """
        correct = (
            ["opls_131"]
            + 2 * ["opls_128", "opls_123"]
            + 2 * ["opls_132"]
            + 6 * ["opls_127"]
        )
        configuration.from_smiles("C(OC)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_129(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 129, hemiacetal oxygen;
        opls 130, hemiacetal hydrogen;
        opls 133, hemiacetal methylene carbon;
        opls 134, hydrogen on acetal methylene carbon
        """
        correct = (
            ["opls_133"]
            + ["opls_128", "opls_123", "opls_129"]
            + 2 * ["opls_134"]
            + 3 * ["opls_127"]
            + ["opls_130"]
        )
        configuration.from_smiles("C(OC)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_135(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 135, acetal methine carbon;
        opls 136, hydrogen on acetal methine carbon
        """
        correct = (
            ["opls_135", "opls_80"]
            + 2 * ["opls_128", "opls_123"]
            + ["opls_136"]
            + 3 * ["opls_85"]
            + 6 * ["opls_127"]
        )
        configuration.from_smiles("C(C)(OC)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_137(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 129, hemiacetal oxygen;
        opls 130, hemiacetal hydrogen;
        opls 137, hemiacetal methine carbon;
        opls 138, hydrogen on acetal methine carbon
        """
        correct = (
            ["opls_137", "opls_80"]
            + ["opls_128", "opls_123", "opls_129"]
            + ["opls_138"]
            + 3 * ["opls_85"]
            + 3 * ["opls_127"]
            + ["opls_130"]
        )
        configuration.from_smiles("C(C)(OC)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_139(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 139, acetal quaternary carbon;
        """
        correct = (
            ["opls_139", "opls_80", "opls_80"]
            + 2 * ["opls_128", "opls_123"]
            + 6 * ["opls_85"]
            + 6 * ["opls_127"]
        )
        configuration.from_smiles("C(C)(C)(OC)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_140(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 128, acetal oxygen;
        opls 129, hemiacetal oxygen;
        opls 130, hemiacetal hydrogen;
        opls 140, hemiacetal quaternary carbon;
        """
        correct = (
            ["opls_140", "opls_80", "opls_80"]
            + ["opls_128", "opls_123", "opls_129"]
            + 6 * ["opls_85"]
            + 3 * ["opls_127"]
            + ["opls_130"]
        )
        configuration.from_smiles("C(C)(C)(OC)O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_142(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 142, thiol sulfur;
        opls 146, thiol hydrogen;
        opls 159, methyl carbon in methyl thiol;
        """
        correct = ["opls_159", "opls_142"] + 3 * ["opls_85"] + ["opls_146"]
        configuration.from_smiles("CS")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_143(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 143, sulfur in H2S;
        opls 147, hydrogen in H2S;
        """
        correct = ["opls_143"] + 2 * ["opls_147"]
        configuration.from_smiles("S")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_144(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, sulfide sulfur;
        opls 151, methyl carbon in methyl sulfide;
        """
        correct = ["opls_144", "opls_151", "opls_151"] + 6 * ["opls_85"]
        configuration.from_smiles("S(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_145(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 145, disulfide sulfur;
        opls 155, methyl carbon in methyl disulfide;
        """
        correct = ["opls_155", "opls_145", "opls_145", "opls_155"] + 6 * ["opls_85"]
        configuration.from_smiles("CSSC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_148(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 142, thiol sulfur;
        opls 146, thiol hydrogen;
        opls 148, methylene carbon adjacent to thiol;
        """
        correct = ["opls_142", "opls_148", "opls_80"] + ["opls_146"] + 5 * ["opls_85"]
        configuration.from_smiles("SCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_149(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 142, thiol sulfur;
        opls 146, thiol hydrogen;
        opls 149, methine carbon adjacent to thiol;
        """
        correct = (
            ["opls_142", "opls_149", "opls_80", "opls_80"]
            + ["opls_146"]
            + 7 * ["opls_85"]
        )
        configuration.from_smiles("SC(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_150(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 142, thiol sulfur;
        opls 146, thiol hydrogen;
        opls 150, quaternary carbon adjacent to thiol;
        """
        correct = (
            ["opls_142", "opls_150"] + 3 * ["opls_80"] + ["opls_146"] + 9 * ["opls_85"]
        )
        configuration.from_smiles("SC(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_152(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, sulfide sulfur;
        opls 152, methylene carbon adjacent to sulfide;
        """
        correct = ["opls_144"] + 2 * ["opls_152", "opls_80"] + 10 * ["opls_85"]
        configuration.from_smiles("S(CC)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed ethyl methyl sulfide
        correct = ["opls_144"] + ["opls_152", "opls_80", "opls_151"] + 8 * ["opls_85"]
        configuration.from_smiles("S(CC)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_153(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, sulfide sulfur;
        opls 153, methine carbon adjacent to thiol;
        """
        correct = (
            ["opls_144"] + 2 * ["opls_153", "opls_80", "opls_80"] + 14 * ["opls_85"]
        )
        configuration.from_smiles("S(C(C)C)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed isopropyl methyl sulfide
        correct = (
            ["opls_144"]
            + ["opls_153", "opls_80", "opls_80", "opls_151"]
            + 10 * ["opls_85"]
        )
        configuration.from_smiles("S(C(C)C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_154(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, sulfide sulfur;
        opls 154, quaternary carbon adjacent to thiol;
        """
        correct = ["opls_144"] + 2 * (["opls_154"] + 3 * ["opls_80"]) + 18 * ["opls_85"]
        configuration.from_smiles("S(C(C)(C)C)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed t-butyl methyl sulfide
        correct = (
            ["opls_144"]
            + (["opls_154"] + 3 * ["opls_80"])
            + ["opls_151"]
            + 12 * ["opls_85"]
        )
        configuration.from_smiles("S(C(C)(C)C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_156(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, disulfide sulfur;
        opls 156, methylene carbon adjacent to disulfide;
        """
        correct = (
            ["opls_80", "opls_156"]
            + 2 * ["opls_145"]
            + ["opls_156", "opls_80"]
            + 10 * ["opls_85"]
        )
        configuration.from_smiles("CCSSCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed ethyl methyl sulfide
        correct = ["opls_80", "opls_156", "opls_145", "opls_145", "opls_155"] + 8 * [
            "opls_85"
        ]
        configuration.from_smiles("CCSSC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_157(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, disulfide sulfur;
        opls 157, methine carbon adjacent to thiol;
        """
        correct = (
            ["opls_157", "opls_80", "opls_80"]
            + 2 * ["opls_145"]
            + ["opls_157", "opls_80", "opls_80"]
            + 14 * ["opls_85"]
        )
        configuration.from_smiles("C(C)(C)SSC(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed isopropyl methyl disulfide
        correct = [
            "opls_157",
            "opls_80",
            "opls_80",
            "opls_145",
            "opls_145",
            "opls_155",
        ] + 10 * ["opls_85"]
        configuration.from_smiles("C(C)(C)SSC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_158(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 144, disulfide sulfur;
        opls 158, quaternary carbon adjacent to thiol;
        """
        correct = (
            (["opls_158"] + 3 * ["opls_80"])
            + 2 * ["opls_145"]
            + (["opls_158"] + 3 * ["opls_80"])
            + 18 * ["opls_85"]
        )
        configuration.from_smiles("C(C)(C)(C)SSC(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # mixed t-butyl methyl disulfide
        correct = (
            (["opls_158"] + 3 * ["opls_80"])
            + 2 * ["opls_145"]
            + ["opls_155"]
            + 12 * ["opls_85"]
        )
        configuration.from_smiles("C(C)(C)(C)SSC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_160(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 160, methylene carbon in benzyl alcohol
        opls 163, phenyl carbon with benzyl alcohol or nitrile
        """
        correct = (
            ["opls_97", "opls_96", "opls_160", "opls_163"]
            + 5 * ["opls_90"]
            + 2 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("[H]OCc1ccccc1", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_161(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 161, methine carbon in benzyl alcohol
        opls 163, phenyl carbon with benzyl alcohol or nitrile
        """
        correct = (
            ["opls_97", "opls_96", "opls_161", "opls_80", "opls_163"]
            + 5 * ["opls_90"]
            + 4 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("[H]OC(C)c1ccccc1", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_162(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 162, quaternary carbon in benzyl alcohol
        opls 163, phenyl carbon with benzyl alcohol or nitrile
        """
        correct = (
            ["opls_97", "opls_96", "opls_162", "opls_80", "opls_80", "opls_163"]
            + 5 * ["opls_90"]
            + 6 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("[H]OC(C)(C)c1ccccc1", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_164(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 151, carbon in methyl sulfide;
        opls 85,  hydrogens on alkane
        opls 164, sulfur in thioanisole;
        opls 170, phenyl carbon in thioanisole
        """
        correct = (
            ["opls_151", "opls_164", "opls_170"]
            + 5 * ["opls_90"]
            + 3 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CSc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_165(oplsaa_assigner, configuration):
        """Test of atom-type assignment force
        opls 165, CA in GLY

        ***NOT TESTED YET***
        """
        pass

    def test_opls_166(oplsaa_assigner, configuration):
        """Test of atom-type assignment force
        opls 166, CA in ALA and most AA

        ***NOT TESTED YET***
        """
        pass

    def test_opls_167(oplsaa_assigner, configuration):
        """Test of atom-type assignment force
        opls 167, CA in AIB (methyl ALA)

        ***NOT TESTED YET***
        """
        pass

    def test_opls_168(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 168, chlorine in chloroalkene Cl-CH=
        opls 169, carbon in chloroalkene, Cl-CH=
        opls 88,  carbon in alkene =CH2
        opls 89,  hydrogens on alkene
        """
        correct = ["opls_168", "opls_169", "opls_88"] + 3 * ["opls_89"]
        configuration.from_smiles("ClC=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Symmetric version
        correct = ["opls_168", "opls_169", "opls_169", "opls_168"] + 2 * ["opls_89"]
        configuration.from_smiles("ClC=CCl")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_173(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 173, carbon in C=O of benzophenone
        opls 223, ketone oxygen >C=O
        """
        correct = ["opls_173", "opls_223"] + 12 * ["opls_90"] + 10 * ["opls_91"]
        configuration.from_smiles("C(=O)(c1ccccc1)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_174(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 174, carbon in C=O of benzaldehyde
        opls 220, aldehyde oxygen -CH=O
        opls 221, aldehyde hydrogen
        """
        correct = (
            ["opls_221", "opls_174", "opls_220"] + 6 * ["opls_90"] + 5 * ["opls_91"]
        )
        configuration.from_smiles("[H]C(=O)c1ccccc1", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_175(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 175, carbon in C=O of acetophenone
        opls 223, ketone oxygen >C=O
        """
        correct = (
            ["opls_175", "opls_223", "opls_80"]
            + 6 * ["opls_90"]
            + 3 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("C(=O)(C)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_219(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 219, carbon aldehyde -CH=O
        opls 220, oxygen in aldehyde -CH=O
        opls 221, hydrogen in aldehyde -CH=O
        """
        correct = ["opls_221", "opls_219", "opls_220", "opls_80"] + 3 * ["opls_85"]
        configuration.from_smiles("[H]C(=O)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_222(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 222, carbon ketone >CH=O
        opls 223, oxygen in ketone >C=O
        """
        correct = ["opls_222", "opls_223", "opls_80", "opls_80"] + 6 * ["opls_85"]
        configuration.from_smiles("C(=O)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Phenyl ethyl ketone
        correct = (
            ["opls_222", "opls_223"]
            + 6 * ["opls_90"]
            + ["opls_81", "opls_80"]
            + 5 * ["opls_91"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("C(=O)(c1ccccc1)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_171(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 171, methine carbon adjacent to N of amide -NH-CHR2
        opls 180, N of amide C(=O)-NHR
        opls 183, H on nitrogen of amide, -NHR
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_180", "opls_171"]
            + 2 * ["opls_80"]
            + 3 * ["opls_85"]
            + ["opls_183"]
            + 7 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)NC(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_172(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 172, quaternary carbon adjacent to N of amide -NH-CR3
        opls 180, N of amide C(=O)-NHR
        opls 183, H on nitrogen of amide, -NHR
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_180", "opls_172"]
            + 3 * ["opls_80"]
            + 3 * ["opls_85"]
            + ["opls_183"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)NC(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_179(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 179, N of amide C(=O)-NH2
        opls 182, H on nitrogen of amide, -NH2
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_179"]
            + 3 * ["opls_85"]
            + 2 * ["opls_182"]
        )
        configuration.from_smiles("CC(=O)N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_181(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 847, N of amide C(=O)-NR2
        opls 845, carbonyl carbon of amide
        opls 846, carbonyl oxygen of amide
        opls 848, methyl carbon on N of amide C(=O)-N-CH3
        opls 852, H of N-alkane group
        """
        correct = (
            ["opls_80", "opls_845", "opls_846", "opls_847"]
            + 2 * ["opls_848"]
            + 3 * ["opls_85"]
            + 6 * ["opls_852"]
        )
        configuration.from_smiles("CC(=O)N(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_184(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 180, N of amide C(=O)-NHR
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        opls 183, H on nitrogen of amide, -NHR
        opls 184, methyl carbon on N of amide C(=O)-NH-CH3
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_180"]
            + ["opls_184"]
            + 3 * ["opls_85"]
            + ["opls_183"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)NC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_186(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 180, N of amide C(=O)-NHR
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        opls 183, H on nitrogen of amide, -NHR
        opls 186, methylene carbon on N of amide C(=O)-NH-CH2R
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_180"]
            + ["opls_186", "opls_80"]
            + 3 * ["opls_85"]
            + ["opls_183"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)NCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_849(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-methylene tertiary amide
        opls 847, N of amide C(=O)-NR2
        opls 845, carbonyl carbon of amide
        opls 846, carbonyl oxygen of amide
        opls 848, methyl carbon of N-methyl tertiary amine
        opls 849, methylene carbon on N of amide C(=O)-NR-CH2R
        opls 852, H on N-alkane carbon
        """
        correct = (
            ["opls_80", "opls_845", "opls_846", "opls_847"]
            + ["opls_848", "opls_849", "opls_80"]
            + 3 * ["opls_85"]
            + 5 * ["opls_852"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)N(C)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_850(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 847, N of amide C(=O)-NR2
        opls 845, carbonyl carbon of amide
        opls 846, carbonyl oxygen of amide
        opls 848, methyl carbon of N-methyl tertiary amine
        opls 850, methine carbon on N of amide C(=O)-NR-CHR2
        opls 852, H on N-alkane carbon
        """
        correct = (
            ["opls_80", "opls_845", "opls_846", "opls_847"]
            + ["opls_848", "opls_850", "opls_80", "opls_80"]
            + 3 * ["opls_85"]
            + 4 * ["opls_852"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)N(C)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_189(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 189, carbonyl carbon of urea H2N-C(=O)-NH2
        opls 190, carbonyl oxygen of urea
        opls 191, N of urea
        opls 192, H on N of urea
        """
        correct = ["opls_189", "opls_190", "opls_191", "opls_191"] + 4 * ["opls_192"]
        configuration.from_smiles("C(=O)(N)(N)")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_193(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 193, nitrogen of imide O=C-HN-C(=O)
        opls 194, carbonyl carbon of imide
        opls 195, carbonyl oxygen of imide
        opls 196, hydrogen on N of imide
        opls 197, H on C of formimide HC(=O)-NH-CH(=O)
        """
        correct = ["opls_195", "opls_194", "opls_193", "opls_194", "opls_195"] + [
            "opls_197",
            "opls_196",
            "opls_197",
        ]
        configuration.from_smiles("O=CNC=O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_198(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 193, nitrogen of imide O=C-HN-C(=O)
        opls 194, carbonyl carbon of imide
        opls 195, carbonyl oxygen of imide
        opls 196, hydrogen on N of imide
        opls 197, H on C of formimide HC(=O)-NH-CH(=O)
        opls 198, methyl group on imide
        """
        correct = (
            ["opls_195", "opls_194", "opls_193", "opls_194", "opls_195", "opls_198"]
            + ["opls_197", "opls_196"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("O=CNC(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # dimethyl imide
        correct = (
            ["opls_193", "opls_196"]
            + 2 * ["opls_194", "opls_195", "opls_198"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("N([H])(C(=O)C)C(=O)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_199(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 193, nitrogen of imide O=C-HN-C(=O)
        opls 194, carbonyl carbon of imide
        opls 195, carbonyl oxygen of imide
        opls 196, hydrogen on N of imide
        opls 197, H on C of formimide HC(=O)-NH-CH(=O)
        opls 199, methylene group on imide
        """
        correct = (
            ["opls_195", "opls_194", "opls_193", "opls_194", "opls_195", "opls_199"]
            + ["opls_80"]
            + ["opls_197", "opls_196"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("O=CNC(=O)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # diethyl imide
        correct = (
            ["opls_193", "opls_196"]
            + 2 * ["opls_194", "opls_195", "opls_199", "opls_80"]
            + 10 * ["opls_85"]
        )
        configuration.from_smiles("N([H])(C(=O)CC)C(=O)CC", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_200(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 193, nitrogen of imide O=C-HN-C(=O)
        opls 194, carbonyl carbon of imide
        opls 195, carbonyl oxygen of imide
        opls 196, hydrogen on N of imide
        opls 197, H on C of formimide HC(=O)-NH-CH(=O)
        opls 200, methine group on imide
        """
        correct = (
            ["opls_195", "opls_194", "opls_193", "opls_194", "opls_195", "opls_200"]
            + 2 * ["opls_80"]
            + ["opls_197", "opls_196"]
            + 7 * ["opls_85"]
        )
        configuration.from_smiles("O=CNC(=O)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # diisopropyl imide
        correct = (
            ["opls_193", "opls_196"]
            + 2 * (["opls_194", "opls_195", "opls_200"] + 2 * ["opls_80"])
            + 14 * ["opls_85"]
        )
        configuration.from_smiles("N([H])(C(=O)C(C)C)C(=O)C(C)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_201(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 193, nitrogen of imide O=C-HN-C(=O)
        opls 194, carbonyl carbon of imide
        opls 195, carbonyl oxygen of imide
        opls 196, hydrogen on N of imide
        opls 197, H on C of formimide HC(=O)-NH-CH(=O)
        opls 201, quaternary carbon on imide
        """
        correct = (
            ["opls_195", "opls_194", "opls_193", "opls_194", "opls_195", "opls_201"]
            + 3 * ["opls_80"]
            + ["opls_197", "opls_196"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("O=CNC(=O)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # diisopropyl imide
        correct = (
            ["opls_193", "opls_196"]
            + 2 * (["opls_194", "opls_195", "opls_201"] + 3 * ["opls_80"])
            + 18 * ["opls_85"]
        )
        configuration.from_smiles(
            "N([H])(C(=O)C(C)(C)C)C(=O)C(C)(C)C", flavor="openbabel"
        )
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_202(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 202, phenyl carbon in benzonitrile, Ar-C#N"
        opls 203, nitrile carbon in benzonitrile, Ar-C#N
        opls 204, nitrogen in benzonitrile, Ar-C#N"
        """
        correct = (
            ["opls_204", "opls_203", "opls_202"] + 5 * ["opls_90"] + 5 * ["opls_91"]
        )
        configuration.from_smiles("N#Cc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_205(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 205, aromatic carbon in chlorobenzene
        opls 206, chlorine in chlorobenzene
        """
        correct = ["opls_206", "opls_205"] + 5 * ["opls_90"] + 5 * ["opls_91"]
        configuration.from_smiles("Clc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_207(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 208, aromatic ring carbon in N-phenylacetamide, CH3-C(=O)-NH-Ar
        opls 207, N of N-phenylacetamide
        opls 177, carbonyl carbon of amide
        opls 178, carbonyl oxygen of amide
        opls 185, methyl carbon on N of amide C(=O)-N-CH3
        opls 183, hydrogen on N or amide C(=O)-NH-R
        """
        correct = (
            ["opls_80", "opls_177", "opls_178", "opls_207", "opls_183", "opls_208"]
            + 5 * ["opls_90"]
            + 3 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CC(=O)N([H])c1ccccc1", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_209(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 209, carbon in carboxylic acid -- -C(=O)-OH
        opls 210, carbonyl oxygen in carboxylic acid
        opls 211, hydroxyl oxygen in carboxylic acid
        opls 212, hydroxyl hydrogen in carboxylic acid
        """
        correct = ["opls_80", "opls_209", "opls_210", "opls_211", "opls_212"] + 3 * [
            "opls_85"
        ]
        configuration.from_smiles("CC(=O)O[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Formic acid is an edge case
        correct = ["opls_221", "opls_209", "opls_210", "opls_211", "opls_212"]
        configuration.from_smiles("[H]C(=O)O[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_213(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 221, hydrogen in aldehydes, formic acid, formamide...
        """
        correct = ["opls_221", "opls_213", "opls_214", "opls_214"]
        configuration.from_smiles("[H]C(=O)[O-]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_215(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 215, methyl carbon adjacent to carboxylate
        """
        correct = ["opls_215", "opls_213", "opls_214", "opls_214"] + 3 * ["opls_85"]
        configuration.from_smiles("CC(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_216(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 216, methylene carbon adjacent to carboxylate
        """
        correct = (
            ["opls_216"]
            + 1 * ["opls_80"]
            + ["opls_213", "opls_214", "opls_214"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("C(C)C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_217(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 217, methine carbon adjacent to carboxylate
        """
        correct = (
            ["opls_217"]
            + 2 * ["opls_80"]
            + ["opls_213", "opls_214", "opls_214"]
            + 7 * ["opls_85"]
        )
        configuration.from_smiles("C(C)(C)C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_218(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 218, quaternary carbon adjacent to carboxylate
        """
        correct = (
            ["opls_218"]
            + 3 * ["opls_80"]
            + ["opls_213", "opls_214", "opls_214"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("C(C)(C)(C)C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_225(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 225, CA in C-terminal AA like ALA
        """
        correct = (
            ["opls_210", "opls_209", "opls_211", "opls_225", "opls_80", "opls_180"]
            + ["opls_183", "opls_177", "opls_178", "opls_80", "opls_212"]
            + 7 * ["opls_85"]
        )
        configuration.from_smiles("O=C(O)C(C)N([H])C(=O)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_226(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 226, CA in C-terminal AA like GLY with no sidechain
        """
        correct = (
            ["opls_210", "opls_209", "opls_211", "opls_226", "opls_180"]
            + ["opls_183", "opls_177", "opls_178", "opls_80", "opls_212"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("O=C(O)CN([H])C(=O)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_227(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 227, CA in C-terminal AA like AIB with two sidechains
        """
        correct = (
            ["opls_210", "opls_209", "opls_211", "opls_227", "opls_80", "opls_80"]
            + ["opls_180", "opls_183", "opls_177", "opls_178", "opls_80", "opls_212"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("O=C(O)C(C)(C)N([H])C(=O)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_228(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 228, CA in C-terminal in PRO
        """
        correct = (
            ["opls_210", "opls_209", "opls_211", "opls_228", "opls_81", "opls_81"]
            + ["opls_849", "opls_847", "opls_845", "opls_846", "opls_80", "opls_212"]
            + ["opls_852"]
            + 4 * ["opls_85"]
            + 2 * ["opls_852"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("O=C(O)C(CCC1)N1C(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_229(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 229, Nitrogen in ammonium cation -- NH4+
        opls 232, Hydrogen in ammonium cation -- NH4+
        """
        correct = ["opls_229"] + 4 * ["opls_232"]
        configuration.from_smiles("[NH4+]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_230(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 230, Nitrogen in ammonium cation -- NH3R+
        opls 233, Hydrogen in ammonium cation -- NH3R+
        opls 234, Methyl carbon adjacent to ammonium cation -- CH3-NH3+
        """
        correct = ["opls_230", "opls_234"] + 3 * ["opls_233"] + 3 * ["opls_85"]
        configuration.from_smiles("[NH3+]C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_231(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 231, Nitrogen in ammonium cation -- NR4+
        opls 888, Methyl carbon adjacent to 4 substituent ammonium cation -- CH3-NR3+
        opls 892, H on methyl adjacent to 4 substituent ammonium cation -- CH3-NR3+
        """
        correct = ["opls_231"] + 4 * ["opls_888"] + 12 * ["opls_892"]
        configuration.from_smiles("[N+](C)(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_240(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 252, Nitrogen in ammonium cation -- NH2R2+
        opls 253, Hydrogen in ammonium cation -- NH2R2+
        opls 240, Methyl carbon adjacent to ammonium cation -- CH3-NH2R+
        """
        correct = (
            ["opls_252", "opls_240", "opls_240"] + 2 * ["opls_253"] + 6 * ["opls_85"]
        )
        configuration.from_smiles("[NH2+](C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_770(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 770, Nitrogen in ammonium cation -- NHR3+
        opls 771, Hydrogen in ammonium cation -- NHR3+
        opls 772, Methyl carbon adjacent to ammonium cation -- CH3-NH2R+
        """
        correct = (
            ["opls_770", "opls_772", "opls_772", "opls_772"]
            + 1 * ["opls_771"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("[NH+](C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_773(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 770, Nitrogen in ammonium cation -- NHR3+
        opls 771, Hydrogen in ammonium cation -- NHR3+
        opls 772, Methyl carbon adjacent to ammonium cation -- CH3-NH2R+
        opls 773, Methylene carbon adjacent to ammonium cation -- -CH2-NH2R+
        """
        correct = (
            ["opls_770", "opls_772", "opls_772", "opls_773", "opls_80"]
            + 1 * ["opls_771"]
            + 11 * ["opls_85"]
        )
        configuration.from_smiles("[NH+](C)(C)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_774(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 770, Nitrogen in ammonium cation -- NHR3+
        opls 771, Hydrogen in ammonium cation -- NHR3+
        opls 772, Methyl carbon adjacent to ammonium cation -- CH3-NH2R+
        opls 774, Methine carbon adjacent to ammonium cation -- >CH-NH2R+
        """
        correct = (
            ["opls_770", "opls_772", "opls_772", "opls_774"]
            + 2 * ["opls_80"]
            + 1 * ["opls_771"]
            + 13 * ["opls_85"]
        )
        configuration.from_smiles("[NH+](C)(C)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_775(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 770, Nitrogen in ammonium cation -- NHR3+
        opls 771, Hydrogen in ammonium cation -- NHR3+
        opls 772, Methyl carbon adjacent to ammonium cation -- CH3-NH2R+
        opls 775, Quaternary carbon adjacent to ammonium cation -- >CH-NH2R+
        """
        correct = (
            ["opls_770", "opls_772", "opls_772", "opls_775"]
            + 3 * ["opls_80"]
            + 1 * ["opls_771"]
            + 15 * ["opls_85"]
        )
        configuration.from_smiles("[NH+](C)(C)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_254(oplsaa_assigner, configuration):
        """Test of atom-type assignment for 1,6 diaminopyridine
        opls 254, aromatic ring N
        opls 255, C2
        opls 256, N in -NH2
        opls 257, H in -NH2
        opls 258, C3
        opls 259, H on C3
        opls 260, C4
        opls 261, H on C4
        """
        correct = (
            ["opls_254", "opls_255", "opls_256", "opls_258", "opls_260"]
            + ["opls_258", "opls_255", "opls_256"]
            + ["opls_257", "opls_257", "opls_259", "opls_261", "opls_259"]
            + ["opls_257", "opls_257"]
        )
        configuration.from_smiles("n1c(N)cccc1(N)")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_342(oplsaa_assigner, configuration):
        """Test of atom-type assignment for chloroalkenes Cl2-C=
        opls 342, Cl
        opls 343, C
        """
        correct = 2 * ["opls_342", "opls_341", "opls_341"]
        configuration.from_smiles("C(Cl)(Cl)=C(Cl)Cl")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed
        correct = ["opls_342", "opls_341", "opls_341", "opls_88", "opls_89", "opls_89"]
        configuration.from_smiles("C(Cl)(Cl)=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_348(oplsaa_assigner, configuration):
        """Test of atom-type assignment for lithium cation -- Li+
        opls 348, Li
        """
        correct = ["opls_348"]
        configuration.from_smiles("[Li+]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_357(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methyl thiolate CH3-S(-)
        opls 357, C
        opls 358, H
        opls 359, S
        """
        correct = ["opls_357", "opls_359"] + 3 * ["opls_358"]
        configuration.from_smiles("C[S-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_360(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methoxide CH3-O(-)
        opls 360, C
        opls 361, H
        opls 362, O
        """
        correct = ["opls_360", "opls_362"] + 3 * ["opls_361"]
        configuration.from_smiles("C[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_363(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methylnitrile anion
        opls 363, C alkane
        opls 364, H alkane
        opls 365, C nitrile
        opls 366, N nitrile
        """
        correct = ["opls_363", "opls_365", "opls_366"] + 2 * ["opls_364"]
        configuration.from_smiles("[CH2-]C#N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_376(oplsaa_assigner, configuration):
        """Test of atom-type assignment for hydroxide anion OH(-)
        opls 376, O
        opls 377, H
        """
        correct = ["opls_376", "opls_377"]
        configuration.from_smiles("[OH-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_378(oplsaa_assigner, configuration):
        """Test of atom-type assignment for uranyl cation UO2++
        opls 378, U
        opls 379, O
        """
        correct = ["opls_379", "opls_378", "opls_379"]
        configuration.from_smiles("O=[U++]=O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_406(oplsaa_assigner, configuration):
        """Test of atom-type assignment for ester -C(=O)-O-R
        opls 406, carbonyl C
        opls 407, carbonyl O
        opls 408, ester O
        opls 409, methyl carbon in methyl ester -O-CH3
        opls 410, alkane ester hydrogen
        """
        correct = (
            ["opls_80", "opls_406", "opls_407", "opls_408", "opls_409"]
            + 3 * ["opls_85"]
            + 3 * ["opls_410"]
        )
        configuration.from_smiles("CC(=O)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_431(oplsaa_assigner, configuration):
        """Test of atom-type assignment for ester -C(=O)-O-CH2-
        opls 406, carbonyl C
        opls 407, carbonyl O
        opls 408, ester O
        opls 431, methylene carbon in alkyl ester -O-CH2-
        opls 410, alkane ester hydrogen
        """
        correct = (
            ["opls_80", "opls_406", "opls_407", "opls_408", "opls_431", "opls_80"]
            + 3 * ["opls_85"]
            + 2 * ["opls_410"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)OCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_432(oplsaa_assigner, configuration):
        """Test of atom-type assignment for ester -C(=O)-O-CH<
        opls 406, carbonyl C
        opls 407, carbonyl O
        opls 408, ester O
        opls 432, methine carbon in alkyl ester -O-CH2-
        opls 410, alkane ester hydrogen
        """
        correct = (
            ["opls_80", "opls_406", "opls_407", "opls_408", "opls_432"]
            + 2 * ["opls_80"]
            + 3 * ["opls_85"]
            + ["opls_410"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)OC(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_433(oplsaa_assigner, configuration):
        """Test of atom-type assignment for ester -C(=O)-O-CR3
        opls 406, carbonyl C
        opls 407, carbonyl O
        opls 408, ester O
        opls 433, quaternary carbon in alkyl ester -O-CH2-
        opls 410, alkane ester hydrogen
        """
        correct = (
            ["opls_80", "opls_406", "opls_407", "opls_408", "opls_433"]
            + 3 * ["opls_80"]
            + 3 * ["opls_85"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)OC(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_411(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzoic acid Ar-C(=O)-OH
        opls 411, carbonyl C
        opls 210, carbonyl O
        opls 211, hydroxyl O
        opls 212, hydroxyl H
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_411", "opls_210", "opls_211", "opls_212"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("c1ccccc1C(=O)O[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_412(oplsaa_assigner, configuration):
        """Test of atom-type assignment for aryl ester Ar-C(=O)-O-R
        opls 412, carbonyl C
        opls 407, carbonyl O
        opls 408, ester O
        opls 409, methyl carbon in methyl ester -O-CH3
        opls 410, alkane ester hydrogen
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_412", "opls_407", "opls_408", "opls_409"]
            + 5 * ["opls_91"]
            + 3 * ["opls_410"]
        )
        configuration.from_smiles("c1ccccc1C(=O)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_413(oplsaa_assigner, configuration):
        """Test of atom-type assignment for phenyl ester -C(=O)-O-Ar
        opls 406, carbonyl C
        opls 407, carbonyl O
        opls 414, ester O
        opls 413, phenyl carbon -O-c<
        """
        correct = (
            ["opls_80", "opls_406", "opls_407", "opls_414", "opls_413"]
            + 5 * ["opls_90"]
            + 3 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CC(=O)Oc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_415(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methyl sulfonamide -- CH3-S(O2)-NH2
        opls 415, S
        opls 416, O
        opls 417, methyl C
        opls 418, methyl H
        opls 419, N
        opls 420, H on N
        """
        correct = (
            ["opls_417", "opls_415", "opls_416", "opls_416", "opls_419"]
            + 3 * ["opls_418"]
            + 2 * ["opls_420"]
        )
        configuration.from_smiles("CS(=O)(=O)N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_421(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-methyl,methyl sulfonamide
        CH3-S(O2)-NH-CH3

        opls 415, S
        opls 416, O
        opls 417, methyl C
        opls 418, methyl H
        opls 421, N
        opls 422, H on -NHR
        opls 423, N-methyl C
        opls 424, N-methyl H
        """
        correct = (
            ["opls_417", "opls_415", "opls_416", "opls_416", "opls_421", "opls_423"]
            + 3 * ["opls_418"]
            + ["opls_422"]
            + 3 * ["opls_424"]
        )
        configuration.from_smiles("CS(=O)(=O)NC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_425(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-ethyl,methyl sulfonamide
        CH3-S(O2)-NH-CH2CH3

        opls 415, S
        opls 416, O
        opls 417, methyl C
        opls 418, methyl H
        opls 421, N
        opls 422, H on -NHR
        opls 425, N-methylene carbon -CH2-
        opls 426, N-methylene hydrogen -CH2-
        opls 427, N-ethyl methyl C
        opls 428, N-ethyl methyl H
        """
        correct = (
            ["opls_417", "opls_415", "opls_416", "opls_416", "opls_421", "opls_425"]
            + ["opls_427"]
            + 3 * ["opls_418"]
            + ["opls_422"]
            + 2 * ["opls_426"]
            + 3 * ["opls_428"]
        )
        configuration.from_smiles("CS(=O)(=O)NCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_429(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-methyl, benzene sulfonamide
        Ar-S(O2)-NH-CH3

        opls 415, S
        opls 416, O
        opls 421, N
        opls 422, H on -NHR
        opls 423, N-methyl C
        opls 424, N-methyl H
        opls 429, aromatic ring carbon
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_429", "opls_415", "opls_416", "opls_416", "opls_421", "opls_423"]
            + 5 * ["opls_91"]
            + ["opls_422"]
            + 3 * ["opls_424"]
        )
        configuration.from_smiles("c1ccccc1S(=O)(=O)NC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_840(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-phenyl, methyl sulfonamide
        CH3-S(O2)-NH-Ar

        opls 415, S
        opls 416, O
        opls 417, methyl C
        opls 418, methyl H
        opls 840, N-phenyl N
        opls 422, H on -NHR
        opls 841, N-phenyl C
        """
        correct = (
            ["opls_417", "opls_415", "opls_416", "opls_416", "opls_840", "opls_841"]
            + 5 * ["opls_90"]
            + 3 * ["opls_418"]
            + ["opls_422"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CS(=O)(=O)Nc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_430(oplsaa_assigner, configuration):
        """Test of atom-type assignment for phenyl,methyl sulfoxide
        CH3-S(O2)-Ar

        opls 430, C in phenyl ring
        opls 436, S
        opls 438, O
        opls 439, methyl C
        """
        correct = (
            ["opls_439", "opls_436", "opls_438", "opls_430"]
            + 5 * ["opls_90"]
            + 3 * ["opls_85"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CS(=O)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_437(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methyl,ethyl sulfoxide
        CH3-S(O2)-CH2-CH3

        opls 437, S in dialkyl sulfoxide
        opls 438, O
        opls 439, methyl C
        opls 440, methylene C
        """
        correct = ["opls_439", "opls_437", "opls_438", "opls_440", "opls_80"] + 8 * [
            "opls_85"
        ]
        configuration.from_smiles("CS(=O)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_434(oplsaa_assigner, configuration):
        """Test of atom-type assignment for sulfone
        -S(O2)-

        opls 434, S
        opls 435, O
        """
        correct = ["opls_80", "opls_434", "opls_435", "opls_435", "opls_80"] + 6 * [
            "opls_85"
        ]
        configuration.from_smiles("CS(=O)(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_458(oplsaa_assigner, configuration):
        """Test of atom-type assignment for a vinyl ether  =CH-OR
        opls 458, C
        """
        correct = (
            ["opls_88", "opls_458", "opls_122", "opls_123"]
            + 3 * ["opls_89"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("C=C-OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_459(oplsaa_assigner, configuration):
        """Test of atom-type assignment for a vinyl ether  =CR-OR
        opls 459, C
        """
        correct = (
            ["opls_88", "opls_459", "opls_80", "opls_122", "opls_123"]
            + 2 * ["opls_89"]
            + 3 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("C=C(C)-OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_460(oplsaa_assigner, configuration):
        """Test of atom-type assignment for biphenyl  Ar-Ar
        opls 460, C
        """
        correct = (
            5 * ["opls_90"] + 2 * ["opls_460"] + 5 * ["opls_90"] + 10 * ["opls_91"]
        )
        configuration.from_smiles("c1ccccc1c2ccccc2")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_461(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyridine
        opls 461, N
        opls 462, C1
        opls 463, C2
        opls 464, C3
        opls 465, H1
        opls 466, H2
        opls 467, H3
        """
        correct = [
            "opls_461",
            "opls_462",
            "opls_463",
            "opls_464",
            "opls_463",
            "opls_462",
        ] + ["opls_465", "opls_466", "opls_467", "opls_466", "opls_465"]
        configuration.from_smiles("n1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_468(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyrazine n1ccncc1
        opls 468, N
        opls 469, C
        opls 470, H
        """
        correct = [
            "opls_468",
            "opls_469",
            "opls_469",
            "opls_468",
            "opls_469",
            "opls_469",
        ] + 4 * ["opls_470"]
        configuration.from_smiles("n1ccncc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_471(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyrimidine n1cnccc1
        opls 471, N
        opls 472, C2
        opls 473, C4
        opls 474, C5
        opls 475, H2
        opls 476, H4
        opls 477, H5
        """
        correct = [
            "opls_471",
            "opls_472",
            "opls_471",
            "opls_473",
            "opls_474",
            "opls_473",
        ] + ["opls_475", "opls_476", "opls_477", "opls_476"]
        configuration.from_smiles("n1cnccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_478(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyridazine n1ncccc1
        opls 478, N
        opls 479, C3
        opls 480, C4
        opls 481, H3
        opls 482, H4
        """
        correct = [
            "opls_478",
            "opls_478",
            "opls_479",
            "opls_480",
            "opls_480",
            "opls_479",
        ] + ["opls_481", "opls_482", "opls_482", "opls_481"]
        configuration.from_smiles("n1ncccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_483(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyrrole n1cccc1
        opls 483, N
        opls 484, C2
        opls 485, C3
        opls 486, HN
        opls 487, HC2
        opls 488, HC3
        """
        correct = ["opls_483", "opls_484", "opls_485", "opls_485", "opls_484"] + [
            "opls_486",
            "opls_487",
            "opls_488",
            "opls_488",
            "opls_487",
        ]
        configuration.from_smiles("N1C=CC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_489(oplsaa_assigner, configuration):
        """Test of atom-type assignment for pyrazole Hn1nccc1
        opls 489, N1
        opls 490, N2
        opls 491, C3
        opls 492, C4
        opls 493, C5
        opls 494, HN1
        opls 495, HC3
        opls 496, HC4
        opls 497, HC5
        """
        correct = ["opls_489", "opls_490", "opls_491", "opls_492", "opls_493"] + [
            "opls_494",
            "opls_495",
            "opls_496",
            "opls_497",
        ]
        configuration.from_smiles("N1N=CC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_498(oplsaa_assigner, configuration):
        """Test of atom-type assignment for imidazole Hn1cncc1
        opls 498, N1
        opls 499, C2
        opls 500, N3
        opls 501, C4
        opls 502, C5
        opls 503, HN1
        opls 504, HC2
        opls 505, HC4
        opls 506, HC5
        """
        correct = ["opls_498", "opls_499", "opls_500", "opls_501", "opls_502"] + [
            "opls_503",
            "opls_504",
            "opls_505",
            "opls_506",
        ]
        configuration.from_smiles("N1C=NC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_507(oplsaa_assigner, configuration):
        """Test of atom-type assignment for furan o1cccc1
        opls 507, O
        opls 508, C2
        opls 509, C3
        opls 510, HC2
        opls 511, HC3
        """
        correct = ["opls_507", "opls_508", "opls_509", "opls_509", "opls_508"] + [
            "opls_510",
            "opls_511",
            "opls_511",
            "opls_510",
        ]
        configuration.from_smiles("O1C=CC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_512(oplsaa_assigner, configuration):
        """Test of atom-type assignment for oxazole o1nccc1
        opls 512, O1
        opls 513, C2
        opls 514, N3
        opls 515, C4
        opls 516, C5
        opls 517, HC2
        opls 518, HC4
        opls 519, HC5
        """
        correct = ["opls_512", "opls_513", "opls_514", "opls_515", "opls_516"] + [
            "opls_517",
            "opls_518",
            "opls_519",
        ]
        configuration.from_smiles("O1C=NC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_520(oplsaa_assigner, configuration):
        """Test of atom-type assignment for isoxazole o1nccc1
        opls 520, O1
        opls 521, N2
        opls 522, C3
        opls 523, C4
        opls 524, C5
        opls 525, HC2
        opls 526, HC4
        opls 527, HC5
        """
        correct = ["opls_520", "opls_521", "opls_522", "opls_523", "opls_524"] + [
            "opls_525",
            "opls_526",
            "opls_527",
        ]
        configuration.from_smiles("O1N=CC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_528(oplsaa_assigner, configuration):
        """Test of atom-type assignment for indole
        opls 528, N1
        opls 529, C2
        opls 530, C3
        opls 531, C4
        opls 532, C5
        opls 533, C6
        opls 534, C7
        opls 535, C8
        opls 536, C9
        opls 537, HN1
        opls 538, HC2
        opls 539, HC3
        opls 540, HC4
        opls 541, HC5
        opls 542, HC6
        opls 543, HC7
        """
        correct = (
            ["opls_528", "opls_537", "opls_529", "opls_530", "opls_535", "opls_531"]
            + ["opls_532", "opls_533", "opls_534", "opls_536"]
            + ["opls_538", "opls_539", "opls_540", "opls_541"]
            + ["opls_542", "opls_543"]
        )
        configuration.from_smiles("n1([H])ccc2ccccc21", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_544(oplsaa_assigner, configuration):
        """Test of atom-type assignment for quinoline
        opls 544, N1
        opls 545, C2
        opls 546, C3
        opls 547, C4
        opls 548, C5
        opls 549, C6
        opls 550, C7
        opls 551, C8
        opls 552, C9
        opls 553, C10
        opls 554, HC2
        opls 555, HC3
        opls 556, HC4
        opls 557, HC5
        opls 558, HC6
        opls 559, HC7
        opls 560, HC8
        """
        correct = (
            ["opls_544", "opls_545", "opls_546", "opls_547", "opls_552"]
            + ["opls_548", "opls_549", "opls_550", "opls_551"]
            + ["opls_553", "opls_554", "opls_555", "opls_556"]
            + ["opls_557", "opls_558", "opls_559", "opls_560"]
        )
        configuration.from_smiles("n1cccc2ccccc21")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_561(oplsaa_assigner, configuration):
        """Test of atom-type assignment for purine
        opls 561, N1
        opls 562, C2
        opls 563, N3
        opls 564, C4
        opls 565, C5
        opls 566, C6
        opls 567, N7
        opls 568, C8
        opls 569, N9
        opls 570, HC2
        opls 571, HC6
        opls 572, HC8
        opls 573, HN9
        """
        correct = (
            ["opls_561", "opls_562", "opls_563", "opls_564", "opls_565"]
            + ["opls_566", "opls_567", "opls_568", "opls_569"]
            + ["opls_573", "opls_570", "opls_571", "opls_572"]
        )
        configuration.from_smiles("n1cnc2c(c1)ncn2[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_574(oplsaa_assigner, configuration):
        """Test of atom-type assignment for thiazole
        opls 574, S1
        opls 575, C2
        opls 576, N3
        opls 577, C4
        opls 578, C5
        opls 579, HC2
        opls 580, HC4
        opls 580, HC5
        """
        correct = ["opls_574", "opls_575", "opls_576", "opls_577", "opls_578"] + [
            "opls_579",
            "opls_580",
            "opls_581",
        ]
        configuration.from_smiles("s1cncc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_582(oplsaa_assigner, configuration):
        """Test of atom-type assignment for 1,3,5-triazine
        opls 582, N
        opls 583, C
        opls 584, HC
        """
        correct = 3 * ["opls_582", "opls_583"] + 3 * ["opls_584"]
        configuration.from_smiles("n1cncnc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_585(oplsaa_assigner, configuration):
        """Test of atom-type assignment for serotonin
        opls 528, N1
        opls 529, C2
        opls 530, C3
        opls 531, C4
        opls 585, C5
        opls 533, C6
        opls 534, C7
        opls 535, C8
        opls 536, C9
        opls 537, HN1
        opls 538, HC2
        opls 540, HC4
        opls 542, HC6
        opls 543, HC7
        """
        correct = (
            ["opls_528", "opls_537", "opls_529", "opls_530"]
            + ["opls_586", "opls_736", "opls_730"]
            + ["opls_535", "opls_531"]
            + ["opls_585", "opls_109", "opls_110", "opls_533", "opls_534", "opls_536"]
            + ["opls_538"]
            + 2 * ["opls_85"]
            + 2 * ["opls_741"]
            + 2 * ["opls_739"]
            + ["opls_540", "opls_542", "opls_543"]
        )
        configuration.from_smiles("n1([H])cc(CCN)c2cc(O[H])ccc21", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_652(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 652, cyclopropane -CH2-
        opls 653, cyclopropane -CHR-
        opls 654, cyclopropane -CR2-
        """
        correct = [
            "opls_652",
            "opls_653",
            "opls_80",
            "opls_654",
            "opls_80",
            "opls_80",
        ] + 12 * ["opls_85"]
        configuration.from_smiles("C1C(C)C1(C)(C)")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_659(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 659, aromatic carbon in fluorobenzene
        opls 660, fluorine in fluorobenzene
        """
        correct = ["opls_660", "opls_659"] + 5 * ["opls_90"] + 5 * ["opls_91"]
        configuration.from_smiles("Fc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_661(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 661, aromatic carbon in hexafluorobenzene
        opls 662, chlorine in hexafluorobenzene
        """
        correct = 6 * ["opls_661", "opls_662"]
        configuration.from_smiles("c1(F)c(F)c(F)c(F)c(F)c1(F)")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_665(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 665, aromatic carbon in trifluoromethylbenzene
        opls 666, methyl carbon in trifluoromethylbenzene
        opls 667, fluorine in trifluoromethylbenzene
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_665", "opls_666"]
            + 3 * ["opls_667"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("c1ccccc1C(F)(F)F")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_668(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 668, aromatic carbon in difluorobenzene
        opls 669, chlorine in difluorobenzene
        """
        correct = 2 * ["opls_668", "opls_669"] + 4 * ["opls_90"] + 4 * ["opls_91"]
        configuration.from_smiles("c1(F)c(F)cccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_670(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 670, aromatic carbon in bromobenzene
        opls 671, bromine in bromobenzene
        """
        correct = ["opls_671", "opls_670"] + 5 * ["opls_90"] + 5 * ["opls_91"]
        configuration.from_smiles("Brc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_672(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 672, aromatic carbon in iodobenzene
        opls 673, fluorine in iodobenzene
        """
        correct = ["opls_673", "opls_672"] + 5 * ["opls_90"] + 5 * ["opls_91"]
        configuration.from_smiles("Ic1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_675(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 676, aromatic carbon in thiophenol
        opls 675, sulfur in thiophenol
        """
        correct = (
            ["opls_675", "opls_676"] + 5 * ["opls_90"] + ["opls_146"] + 5 * ["opls_91"]
        )
        configuration.from_smiles("Sc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_694(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 695, carbon in alkyl nitrile
        opls 694, nitrogen in alkyl nitrile
        opls 696, methyl carbon in acetonitrile
        opls 700, H adjacent to alkyl nitrile
        """
        correct = ["opls_694", "opls_695", "opls_696"] + 3 * ["opls_700"]
        configuration.from_smiles("N#CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_697(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 695, carbon in alkyl nitrile
        opls 694, nitrogen in alkyl nitrile
        opls 697, methylene carbon in alkyl nitrile
        opls 700, H adjacent to alkyl nitrile
        """
        correct = (
            ["opls_694", "opls_695", "opls_697", "opls_80"]
            + 2 * ["opls_700"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("N#CCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_698(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 695, carbon in alkyl nitrile
        opls 694, nitrogen in alkyl nitrile
        opls 698, methine carbon in alkyl nitrile
        opls 700, H adjacent to alkyl nitrile
        """
        correct = (
            ["opls_694", "opls_695", "opls_698"]
            + 2 * ["opls_80"]
            + ["opls_700"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("N#CC(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_699(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 695, carbon in alkyl nitrile
        opls 694, nitrogen in alkyl nitrile
        opls 698, quaternary carbon in alkyl nitrile
        """
        correct = (
            ["opls_694", "opls_695", "opls_699"] + 3 * ["opls_80"] + 9 * ["opls_85"]
        )
        configuration.from_smiles("N#CC(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_701(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 701, nitrogen in alkyl nitro group
        opls 702, oxygen in alkyl nitro group
        opls 703, methyl carbon in nitromethane
        opls 704, H adjacent to alkyl nitro group
        """
        correct = ["opls_701", "opls_702", "opls_702", "opls_703"] + 3 * ["opls_704"]
        configuration.from_smiles("N(=O)(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_705(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 701, nitrogen in alkyl nitro group
        opls 702, oxygen in alkyl nitro group
        opls 705, methylene carbon adjacent to an nitro group
        opls 704, H adjacent to alkyl nitro group
        """
        correct = (
            ["opls_701", "opls_702", "opls_702", "opls_705", "opls_80"]
            + 2 * ["opls_704"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("N(=O)(=O)CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_706(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 701, nitrogen in alkyl nitro group
        opls 702, oxygen in alkyl nitro group
        opls 706, methine carbon adjacent to an nitro group
        opls 704, H adjacent to alkyl nitro group
        """
        correct = (
            ["opls_701", "opls_702", "opls_702", "opls_706"]
            + 2 * ["opls_80"]
            + ["opls_704"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("N(=O)(=O)C(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_707(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 701, nitrogen in alkyl nitro group
        opls 702, oxygen in alkyl nitro group
        opls 707, quaternary carbon adjacent to an nitro group
        opls 704, H adjacent to alkyl nitro group
        """
        correct = (
            ["opls_701", "opls_702", "opls_702", "opls_707"]
            + 3 * ["opls_80"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("N(=O)(=O)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_708(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 708, nitrogen in nitrobenzene
        opls 702, oxygen in nitro group
        opls 709, aromatic carbon in nitrobenzene
        """
        correct = (
            ["opls_708", "opls_702", "opls_702", "opls_709"]
            + 5 * ["opls_90"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("N(=O)(=O)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_710(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 710, carbon in benzonitrile -- methylene in phenylacetonitrile?
        opls 694, nitrogen in nitrile
        """
        correct = (
            ["opls_694", "opls_695", "opls_710", "opls_163"]
            + 5 * ["opls_90"]
            + 2 * ["opls_700"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("N#CCc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_712(oplsaa_assigner, configuration):
        """Test of atom-type assignment for propylene carbonate
        opls 712, carbonyl oxygen
        opls 713, carbonyl carbon
        opls 714, ester oxygen
        opls 715, methylene -CH2- (C4)
        opls 716, methine -CHR2  (C4')
        opls 717, methyl carbon
        opls 718, hydrogen on methylene (HC4)
        opls 719, hydrogen on methine (HC4')
        opls 720, hydrogen on methyl
        """
        correct = (
            ["opls_714", "opls_713", "opls_712", "opls_714", "opls_716", "opls_717"]
            + ["opls_715"]
            + ["opls_719"]
            + 3 * ["opls_720"]
            + 2 * ["opls_718"]
        )
        configuration.from_smiles("O1C(=O)OC(C)C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_715(oplsaa_assigner, configuration):
        """Test of atom-type assignment for ethylene carbonate
        opls 712, carbonyl oxygen
        opls 713, carbonyl carbon
        opls 714, ester oxygen
        opls 715, methylene -CH2- (C4)
        opls 718, hydrogen on methylene (HC4)
        """
        correct = (
            ["opls_714", "opls_713", "opls_712", "opls_714", "opls_715", "opls_715"]
            + 2 * ["opls_718"]
            + 2 * ["opls_718"]
        )
        configuration.from_smiles("O1C(=O)OCC1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_715_F(oplsaa_assigner, configuration):
        """Test of atom-type assignment for fluoroethylene carbonate
        opls 712, carbonyl oxygen
        opls 713, carbonyl carbon
        opls 714, ester oxygen
        opls 715, methylene -CH2- (C4)
        opls 718, hydrogen on methylene (HC4)
        """
        correct = (
            ["opls_714", "opls_713", "opls_712", "opls_714", "opls_789", "opls_786"]
            + ["opls_715"]
            + ["opls_788"]
            + 2 * ["opls_718"]
        )
        configuration.from_smiles("O1C(=O)OC(F)C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_730(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methyl amine
        opls 730, amine N with 2 H's
        opls 733, methyl C
        opls 739, H on -NH2
        opls 741, H on C adjacent to amine N
        """
        correct = ["opls_733", "opls_730"] + 3 * ["opls_741"] + 2 * ["opls_739"]
        configuration.from_smiles("CN")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_731(oplsaa_assigner, configuration):
        """Test of atom-type assignment for methyl ethyl amine
        opls 731, amine N with 1 H
        opls 734, methyl C CH3-NHR
        opls 737, -CH2- on -NHR
        opls 740, H on -NHR
        opls 741, H on C adjacent to amine N
        """
        correct = (
            ["opls_734", "opls_731", "opls_737", "opls_80"]
            + 3 * ["opls_741"]
            + ["opls_740"]
            + 2 * ["opls_741"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CNCC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_746(oplsaa_assigner, configuration):
        """Test of atom-type assignment for aniline (Ar-NH2)
        opls 730, amine N with 2 H
        opls 739, H on -NH2
        opls 746, C in aromatic ring adjacent to amine N
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_746", "opls_730"]
            + 5 * ["opls_91"]
            + 2 * ["opls_739"]
        )
        configuration.from_smiles("c1ccccc1N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_747(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-methyl aniline (Ar-NH-CH3)
        opls 731, amine N with 1 H
        opls 734, methyl carbon on -NHR
        opls 740, H on -NHR
        opls 741, H on alkane-N<
        opls 747, C in aromatic ring adjacent to amine N
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_747", "opls_731", "opls_734"]
            + 5 * ["opls_91"]
            + ["opls_740"]
            + 3 * ["opls_741"]
        )
        configuration.from_smiles("c1ccccc1NC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_748(oplsaa_assigner, configuration):
        """Test of atom-type assignment for N-dimethyl aniline (Ar-N-(CH3)2)
        opls 732, amine N with no H
        opls 735, methyl carbon on -NR2
        opls 741, H on alkane-N<
        opls 748, C in aromatic ring adjacent to amine N
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_748", "opls_732", "opls_735", "opls_735"]
            + 5 * ["opls_91"]
            + 6 * ["opls_741"]
        )
        configuration.from_smiles("c1ccccc1N(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_749(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl amine (Ar-CH2-NH2)
        opls 730, amine N with  2 H's
        opls 739, H on amine -NH2
        opls 741, H on alkane-N<
        opls 749, methylene carbon between phenyl ring and amine group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_749", "opls_730"]
            + 5 * ["opls_91"]
            + 2 * ["opls_741"]
            + 2 * ["opls_739"]
        )
        configuration.from_smiles("c1ccccc1CN")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_754(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl amine (Ar-CH2-NHR)
        opls 731, amine N with 1 H
        opls 731, methyl amine with 1 H CH3-NHR
        opls 740, H on amine -NHR
        opls 741, H on alkane-N<
        opls 754, methylene carbon between phenyl ring and N-substituted amine group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_754", "opls_731", "opls_734"]
            + 5 * ["opls_91"]
            + 2 * ["opls_741"]
            + ["opls_740"]
            + 3 * ["opls_741"]
        )
        configuration.from_smiles("c1ccccc1CNC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_750(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl amine (Ar-CHR-NH2)
        opls 730, amine N with 2 H's
        opls 739, H on amine -NH2
        opls 741, H on alkane-N<
        opls 750, methine carbon between phenyl ring and amine group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_750", "opls_80", "opls_730"]
            + 5 * ["opls_91"]
            + ["opls_741"]
            + 3 * ["opls_85"]
            + 2 * ["opls_739"]
        )
        configuration.from_smiles("c1ccccc1C(C)N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_751(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl amine (Ar-CR2-NH2)
        opls 730, amine N with 2 H's
        opls 739, H on amine -NH2
        opls 751, quaternary carbon between phenyl ring and amine group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_751", "opls_80", "opls_80", "opls_730"]
            + 5 * ["opls_91"]
            + 6 * ["opls_85"]
            + 2 * ["opls_739"]
        )
        configuration.from_smiles("c1ccccc1C(C)(C)N")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_752(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl ether (Ar-CH2-O-R)
        opls 122, O in ether
        opls 123, C in methyl ether
        opls 127, H on alkane in ether
        opls 752, methylene carbon between phenyl ring and ether
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_752", "opls_122", "opls_123"]
            + 5 * ["opls_91"]
            + 5 * ["opls_127"]
        )
        configuration.from_smiles("c1ccccc1COC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_753(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl sulfide (Ar-CH2-S-R)
        opls 144, S in ether
        opls 151, C in methyl sulfide
        opls 752, methylene carbon between phenyl ring and sulfur
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_753", "opls_144", "opls_151"]
            + 5 * ["opls_91"]
            + 5 * ["opls_85"]
        )
        configuration.from_smiles("c1ccccc1CSC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_755(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyne carbon with H (HC#C-))
        opls 755, C
        opls 756, H
        """
        correct = ["opls_755", "opls_755", "opls_756", "opls_756"]
        configuration.from_smiles("C#C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_757(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyne carbon with  (RC#CH-))
        opls 755, C
        opls 756, H
        opls 757, RC#CH R methyl, methylene
        opls 760, alkane H adjacent to alkyne
        """
        correct = ["opls_80", "opls_757", "opls_755"] + 3 * ["opls_760"] + ["opls_756"]
        configuration.from_smiles("CC#C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_758(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyne carbon with methine (RC#CH))
        opls 755, C
        opls 756, H
        opls 758, RC#CH R methine carbon
        opls 760, alkane H adjacent to alkyne
        """
        correct = (
            ["opls_82", "opls_80", "opls_80", "opls_758", "opls_755"]
            + ["opls_760"]
            + 6 * ["opls_85"]
            + ["opls_756"]
        )
        configuration.from_smiles("C(C)(C)C#C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_759(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyne carbon with quaternary carbon (RC#CH)
        opls 755, C
        opls 756, H
        opls 759, RC#CH R quaternary carbon
        """
        correct = (
            ["opls_84", "opls_80", "opls_80", "opls_80", "opls_759", "opls_755"]
            + 9 * ["opls_85"]
            + ["opls_756"]
        )
        configuration.from_smiles("C(C)(C)(C)C#C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_776(oplsaa_assigner, configuration):
        """Test of atom-type assignment for 2-phenylfuran o1c(c2ccccc2)ccc1
        opls 507, O
        opls 776, C2 - phenyl
        opls 777, C3
        opls 778, C2'
        opls 779, C3'
        opls 510, HC2
        opls 511, HC3
        """
        correct = (
            ["opls_507", "opls_776", "opls_460"]
            + 5 * ["opls_90"]
            + ["opls_777", "opls_779", "opls_778"]
            + 5 * ["opls_91"]
            + ["opls_511", "opls_511", "opls_510"]
        )
        configuration.from_smiles("O1C(c2ccccc2)=CC=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_786(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl fluoride
        opls 786, alkyl fluoride
        opls 787, C of methyl group -CH2F
        opls 788, H on fluorinated alkane
        opls 789, C of fluorinated methylene -CHF-
        opls 790, C of fluorinated tertiary carbon
        """
        correct = (
            ["opls_790", "opls_786", "opls_80", "opls_80", "opls_789", "opls_786"]
            + ["opls_787", "opls_786"]
            + 6 * ["opls_85"]
            + 3 * ["opls_788"]
        )
        configuration.from_smiles("C(F)(C)(C)C(F)CF")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_791(oplsaa_assigner, configuration):
        """Test of atom-type assignment perfluoralkane
        opls 791, C of perfluoromethyl group -CF3
        opls 792, C of perfluorinated methylene -CF2-
        opls 793, C of perfluorinated tertiary carbon >CF-
        opls 794, C of tetrafluoromethane
        opls 795, F of perfluorinated alkane
        """
        correct = (
            ["opls_84"]
            + ["opls_791"]
            + 3 * ["opls_795"]
            + ["opls_792"]
            + 2 * ["opls_795"]
            + ["opls_791"]
            + 3 * ["opls_795"]
            + ["opls_793", "opls_795"]
            + 2 * (["opls_791"] + 3 * ["opls_795"])
            + ["opls_791"]
            + 3 * ["opls_795"]
        )
        configuration.from_smiles(
            "C" "(C(F)(F)F)" "(C(F)(F)C(F)(F)F)" "(C(F)(C(F)(F)F)C(F)(F)F)" "C(F)(F)F"
        )
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_796(oplsaa_assigner, configuration):
        """Test of atom-type assignment for difluoromethylbenzene
        opls 796, carbon on difluoromethyl group
        opls 797, hydrogen on difluoromethyl group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_796", "opls_786", "opls_786"]
            + 5 * ["opls_91"]
            + ["opls_797"]
        )
        configuration.from_smiles("c1ccccc1C(F)F")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_798(oplsaa_assigner, configuration):
        """Test of atom-type assignment for fluoroacetate
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 798, fluoromethyl carbon adjacent to carboxylate
        """
        correct = ["opls_798", "opls_786", "opls_213", "opls_214", "opls_214"] + 2 * [
            "opls_788"
        ]
        configuration.from_smiles("C(F)C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_799(oplsaa_assigner, configuration):
        """Test of atom-type assignment for chloroacetate
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 799, chloromethyl carbon adjacent to carboxylate
        """
        correct = ["opls_799", "opls_800", "opls_213", "opls_214", "opls_214"] + 2 * [
            "opls_802"
        ]
        configuration.from_smiles("C(Cl)C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_800(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl chloride
        opls 800, alkyl chloride
        opls 801, C of methyl group -CH2Cl
        opls 802, H on chlorinated alkane
        opls 803, C of chlorinated methylene -CHCl-
        opls 804, C of chlorinated tertiary carbon
        """
        correct = (
            ["opls_804", "opls_800", "opls_80", "opls_80", "opls_803", "opls_800"]
            + ["opls_801", "opls_800"]
            + 6 * ["opls_85"]
            + 3 * ["opls_802"]
        )
        configuration.from_smiles("C(Cl)(C)(C)C(Cl)CCl")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_805(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl bromide
        opls 805, alkyl bromide
        opls 806, C of methyl group -CH2Br
        opls 807, H on brominated alkane
        opls 808, C of brominated methylene -CHBr-
        opls 809, C of brominated tertiary carbon
        """
        correct = (
            ["opls_809", "opls_805", "opls_80", "opls_80", "opls_808", "opls_805"]
            + ["opls_806", "opls_805"]
            + 6 * ["opls_85"]
            + 3 * ["opls_807"]
        )
        configuration.from_smiles("C(Br)(C)(C)C(Br)CBr")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_810(oplsaa_assigner, configuration):
        """Test of atom-type assignment for acyl fluoride F-C=O
        opls 219, carbon aldehyde -CH=O
        opls 220, oxygen in aldehyde -CH=O
        opls 810, fluorine in acyl halide -C(=O)F
        """
        correct = ["opls_810", "opls_219", "opls_220", "opls_80"] + 3 * ["opls_85"]
        configuration.from_smiles("FC(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_811(oplsaa_assigner, configuration):
        """Test of atom-type assignment for acyl chloride Cl-C=O
        opls 219, carbon aldehyde -CH=O
        opls 220, oxygen in aldehyde -CH=O
        opls 811, chlorine in acyl halide -C(=O)Cl
        """
        correct = ["opls_811", "opls_219", "opls_220", "opls_80"] + 3 * ["opls_85"]
        configuration.from_smiles("ClC(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_812(oplsaa_assigner, configuration):
        """Test of atom-type assignment for acyl bromide Br-C=O
        opls 219, carbon aldehyde -CH=O
        opls 220, oxygen in aldehyde -CH=O
        opls 812, bromine in acyl halide -C(=O)Br
        """
        correct = ["opls_812", "opls_219", "opls_220", "opls_80"] + 3 * ["opls_85"]
        configuration.from_smiles("BrC(=O)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_813(oplsaa_assigner, configuration):
        """Test of atom-type assignment for trifluoroanisole C-OCF3
        opls 813, phenyl carbon in anisole
        opls 814, oxygen in anisole;
        opls 815, carbon in trifluoromethyl group;
        opls 816, fluorine in trifluoromethyl group;
        """
        correct = (
            ["opls_815"]
            + 3 * ["opls_816"]
            + ["opls_814", "opls_813"]
            + 5 * ["opls_90"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("C(F)(F)(F)Oc1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_817(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        N-methyl,N-phenylacetamide, CH3-C(=O)-N(CH3)-Ar

        opls 818, aromatic ring carbon in
        opls 817, N of N-phenylacetamide
        opls 845, carbonyl carbon of amide
        opls 846, carbonyl oxygen of amide
        opls 848, methyl carbon on N of amide C(=O)-N-CH3
        opls 852, hydrogen adjacent to tertiary amide
        """
        correct = (
            ["opls_80", "opls_845", "opls_846", "opls_817", "opls_848", "opls_818"]
            + 5 * ["opls_90"]
            + 3 * ["opls_85"]
            + 3 * ["opls_852"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("CC(=O)N(C)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_819(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl amine (Ar-CH2-NR2)
        opls 732, amine N with no H
        opls 735, methyl amine with 1 H CH3-NR2
        opls 741, H on alkane-N<
        opls 819, methylene carbon between phenyl ring and N,N-substituted amine group
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_819", "opls_732", "opls_735", "opls_735"]
            + 5 * ["opls_91"]
            + 8 * ["opls_741"]
        )
        configuration.from_smiles("c1ccccc1CN(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_820(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl hydroxamic acid -C(=O)-N(OH)-
        opls 820, carbonyl carbon in alkyl hydroxamic acid
        opls 822, carbonyl oxygen
        opls 823, nitrogen
        opls 824, HN
        opls 825, hydroxyl oxygen
        opls 826, hydroxyl hydrogen
        """
        correct = (
            ["opls_80", "opls_820", "opls_822", "opls_823", "opls_825", "opls_826"]
            + ["opls_824"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)N(O[H])[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_821(oplsaa_assigner, configuration):
        """Test of atom-type assignment for aryl hydroxamic acid -C(=O)-N(OH)-
        opls 821, carbonyl carbon in aryl hydroxamic acid
        opls 822, carbonyl oxygen
        opls 823, nitrogen
        opls 824, HN
        opls 825, hydroxyl oxygen
        opls 826, hydroxyl hydrogen
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_821", "opls_822", "opls_823", "opls_825", "opls_826"]
            + ["opls_824"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("c1ccccc1C(=O)N(O[H])[H]", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_820a(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl hydroxamic acid -C(=O)-N(OH)-
        opls 820, carbonyl carbon in alkyl hydroxamic acid
        opls 822, carbonyl oxygen
        opls 823, nitrogen
        opls 825, hydroxyl oxygen
        opls 826, hydroxyl hydrogen
        """
        correct = (
            ["opls_80", "opls_820", "opls_822", "opls_823", "opls_825", "opls_826"]
            + ["opls_185"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("CC(=O)N(O[H])C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_827(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl ether (Ar-CHR-O-R)
        opls 122, O in ether
        opls 123, C in methyl ether
        opls 127, H on alkane in ether
        opls 827, tertiary carbon between phenyl ring and ether
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_827", "opls_80", "opls_122", "opls_123"]
            + 5 * ["opls_91"]
            + ["opls_127"]
            + 3 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("c1ccccc1C(C)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_828(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzyl ether (Ar-CR2-O-R)
        opls 122, O in ether
        opls 123, C in methyl ether
        opls 127, H on alkane in ether
        opls 828, tertiary carbon between phenyl ring and ether
        """
        correct = (
            6 * ["opls_90"]
            + ["opls_828", "opls_80", "opls_80", "opls_122", "opls_123"]
            + 5 * ["opls_91"]
            + 6 * ["opls_85"]
            + 3 * ["opls_127"]
        )
        configuration.from_smiles("c1ccccc1C(C)(C)OC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_829(oplsaa_assigner, configuration):
        """Test of atom-type assignment for 3-phenyl pyrrole
        opls 483, N
        opls 484, C2
        opls 829, C3
        opls 830, C3'
        opls 486, HN
        opls 487, HC2
        opls 488, HC3
        """
        correct = (
            ["opls_483", "opls_484", "opls_829", "opls_460"]
            + 5 * ["opls_90"]
            + ["opls_830", "opls_484"]
            + ["opls_486", "opls_487"]
            + 5 * ["opls_91"]
            + ["opls_488", "opls_487"]
        )
        configuration.from_smiles("N1C=C(c2ccccc2)C=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_831(oplsaa_assigner, configuration):
        """Test of atom-type assignment for 4-phenyl imidazole
        opls 498, N1
        opls 499, C2
        opls 500, N3
        opls 831, C4
        opls 832, C5
        opls 503, HN1
        opls 504, HC2
        opls 505, HC4
        opls 506, HC5
        """
        correct = (
            ["opls_498", "opls_499", "opls_500", "opls_831", "opls_460"]
            + 5 * ["opls_90"]
            + ["opls_832"]
            + ["opls_503", "opls_504"]
            + 5 * ["opls_91"]
            + ["opls_506"]
        )
        configuration.from_smiles("N1C=NC(-c2ccccc2)=C1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_833(oplsaa_assigner, configuration):
        """Test of atom-type assignment for diphenylmethane
        opls 833, ring carbon in diphenylmethane
        """
        correct = (
            ["opls_81"]
            + 2 * (["opls_833"] + 5 * ["opls_90"])
            + 2 * ["opls_85"]
            + 10 * ["opls_91"]
        )
        configuration.from_smiles("C(c1ccccc1)c1ccccc1")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_835(oplsaa_assigner, configuration):
        """Test of atom-type assignment for alkyl iodide
        opls 835, alkyl iodide
        opls 836, C of methyl group -CH2I
        opls 837, C of iodinated methylene -CHI-
        opls 838, C of iodinated tertiary carbon
        opls 839, H on iodinated alkane
        """
        correct = (
            ["opls_838", "opls_835", "opls_80", "opls_80", "opls_837", "opls_835"]
            + ["opls_836", "opls_835"]
            + 6 * ["opls_85"]
            + 3 * ["opls_839"]
        )
        configuration.from_smiles("C(I)(C)(C)C(I)CI")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_842(oplsaa_assigner, configuration):
        """Test of atom-type assignment for benzoate
        opls 213, carbon in carboxylate -- -C(-O)-O(-)
        opls 214, oxygen in carboxylate
        opls 842, ring carbon adjacent to carboxylate
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_842", "opls_213", "opls_214", "opls_214"]
            + 5 * ["opls_91"]
        )
        configuration.from_smiles("c1ccccc1C(=O)[O-]")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_843(oplsaa_assigner, configuration):
        """Test of atom-type assignment for
        opls 189, carbonyl carbon of urea H2N-C(=O)-NH2
        opls 190, carbonyl oxygen of urea
        opls 191, N of urea
        opls 192, H on N of urea
        opls 843, N of N-phenyl urea
        opls 844, ring carbon of N-phenyl urea
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_844", "opls_843", "opls_189", "opls_190"]
            + ["opls_191"]
            + 5 * ["opls_91"]
            + 3 * ["opls_192"]
        )
        configuration.from_smiles("c1ccccc1NC(=O)(N)")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            assert result == correct

    def test_opls_853(oplsaa_assigner, configuration):
        """Test of atom-type assignment for tertiary formamide
        HC(=O)N(CH3)CH2CH3
        opls 853, carbonyl carbon
        opls 854, carbonyl oxygen
        opls 855, formyl hydrogen
        opls 847, tertiary nitrogen
        opls 848, N-methyl carbon on amide N
        opls 849, N-methylene carbon on amide N
        opls 852, alkane hydrogen adjacent to amide N
        """
        correct = (
            ["opls_855", "opls_853", "opls_854", "opls_847", "opls_848", "opls_849"]
            + ["opls_80"]
            + 5 * ["opls_852"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("[H]C(=O)N(C)CC", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            assert result == correct

    def test_opls_850b(oplsaa_assigner, configuration):
        """Test of atom-type assignment for tertiary formamide
        HC(=O)N(CH3)CH2CH3
        opls 853, carbonyl carbon
        opls 854, carbonyl oxygen
        opls 855, formyl hydrogen
        opls 847, tertiary nitrogen
        opls 848, N-methyl carbon on amide N
        opls 850, N-methine carbon on amide N
        opls 852, alkane hydrogen adjacent to amide N
        """
        correct = (
            ["opls_855", "opls_853", "opls_854", "opls_847", "opls_848", "opls_850"]
            + 2 * ["opls_80"]
            + 4 * ["opls_852"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("[H]C(=O)N(C)C(C)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            assert result == correct

    def test_opls_866(oplsaa_assigner, configuration):
        """Test of atom-type assignment for quaternary silane
        methyl, ethyl, isopropyl, t-butyl silane
        opls 866, silane silicon R4-Si
        opls 870, alkane hydrogen adjacent to silicon
        opls 871, methyl silane
        opls 872, methylene silane
        opls 873, methine silane
        opls 874, quaternary carbon on silane
        """
        correct = (
            ["opls_866"]
            + ["opls_871"]
            + ["opls_872"]
            + ["opls_80"]
            + ["opls_873"]
            + 2 * ["opls_80"]
            + ["opls_874"]
            + 3 * ["opls_80"]
            + 3 * ["opls_870"]
            + 2 * ["opls_870"]
            + 3 * ["opls_85"]
            + 1 * ["opls_870"]
            + 6 * ["opls_85"]
            + 9 * ["opls_85"]
        )
        configuration.from_smiles("[Si](C)(CC)(C(C)C)C(C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            assert result == correct

    def test_opls_893(oplsaa_assigner, configuration):
        """Test of atom-type assignment for anilinium ion Ar-NR4+
        opls 888, carbon of methyl ammonium quaternary ion
        opls 892: hydrogen of methyl ammonium quaternary ion
        opls 893, nitrogen
        opls 894, ring carbon,
        """
        correct = (
            5 * ["opls_90"]
            + ["opls_894", "opls_893"]
            + 3 * ["opls_888"]
            + 5 * ["opls_91"]
            + 9 * ["opls_892"]
        )
        configuration.from_smiles("c1ccccc1[N+](C)(C)C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            assert result == correct

    def test_opls_897(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 897,  middle bond of triene
        C=CR-CR=CR-CR=C

        opls_89: H in =CH-
        opls_95: C in =CH-C=
        opls_120: C in =CR-C=
        opls_897: C in middle triene bond =C-CR=CR-C=
        """
        correct = (
            ["opls_88", "opls_95", "opls_897", "opls_80", "opls_897", "opls_80"]
            + ["opls_95", "opls_88"]
            + 3 * ["opls_89"]
            + 6 * ["opls_85"]
            + 3 * ["opls_89"]
        )
        configuration.from_smiles("C=CC(C)=C(C)C=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_898(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 897,  middle bond of triene
        C=CH-CH=CH-CH=C

        opls_89: H in =CH-
        opls_95: C in =CH-C=
        opls_120: C in =CR-C=
        opls_897: C in middle triene bond =C-CR=CR-C=
        opls_898: C in middle triene bond =C-CH=CH-C=
        """
        correct = (
            ["opls_88", "opls_95", "opls_898", "opls_898", "opls_95", "opls_88"]
            + 4 * ["opls_89"]
            + 4 * ["opls_89"]
        )
        configuration.from_smiles("C=CC=CC=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # Mixed
        correct = (
            ["opls_88", "opls_95", "opls_897", "opls_80", "opls_898"]
            + ["opls_95", "opls_88"]
            + 3 * ["opls_89"]
            + 3 * ["opls_85"]
            + 4 * ["opls_89"]
        )
        configuration.from_smiles("C=CC(C)=CC=C")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_900(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 897,  allene
        H2C=C=CH2

        opls_899: H in =C=CH-
        opls_900: terminal C in =C=CH2
        opls_903: central C  =C=
        """
        correct = ["opls_900", "opls_903", "opls_900"] + 4 * ["opls_899"]
        configuration.from_smiles("C=C=C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_904(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 897,  ketene
        H2C=C=O

        opls_899: H in =C=CH-
        opls_900: terminal C in =C=CH2
        opls_904: central C  =C=
        opls_905: oxygen in carbonyl
        """
        correct = ["opls_900", "opls_904", "opls_905"] + 2 * ["opls_899"]
        configuration.from_smiles("C=C=O")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_901(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 901,  allene
        H2C=C=CH-CH3

        opls_899: H in =C=CH-
        opls_901: terminal C in =C=CH-C
        opls_903: central C  =C=
        """
        correct = (
            ["opls_900", "opls_903", "opls_901", "opls_80"]
            + 3 * ["opls_899"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("C=C=CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # symmetric
        correct = (
            ["opls_80", "opls_901", "opls_903", "opls_901", "opls_80"]
            + 3 * ["opls_85"]
            + 2 * ["opls_899"]
            + 3 * ["opls_85"]
        )
        configuration.from_smiles("CC=C=CC")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

    def test_opls_902(oplsaa_assigner, configuration):
        """Test of atom-type assignment for opls 903,  allene
        H2C=C=CR2

        opls_899: H in =C=CH-
        opls_902: terminal C in =C=CR2
        opls_903: central C  =C=
        """
        correct = (
            ["opls_900", "opls_903", "opls_902", "opls_80", "opls_80"]
            + 2 * ["opls_899"]
            + 6 * ["opls_85"]
        )
        configuration.from_smiles("C=C=C(C)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")

        # symmetric
        correct = (
            ["opls_80", "opls_902", "opls_80", "opls_903", "opls_902"]
            + ["opls_80", "opls_80"]
            + 12 * ["opls_85"]
        )
        configuration.from_smiles("CC(C)=C=C(C)C", flavor="openbabel")
        result = oplsaa_assigner.assign(configuration)
        if result != correct:
            print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
            raise AssertionError(f"\n result: {result}\ncorrect: {correct}")
