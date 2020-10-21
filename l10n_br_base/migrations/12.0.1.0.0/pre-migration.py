# Copyright 2018 KMEE INFORMATICA LTDA - Gabriel Cardoso de Faria
# Copyright (C) 2020 - TODAY Magno Costa - Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_xml_ids_banks_renames = [
    ("l10n_br_base.res_bank_1", "l10n_br_base.res_bank_001"),
    ("l10n_br_base.res_bank_2", "l10n_br_base.res_bank_003"),
    ("l10n_br_base.res_bank_3", "l10n_br_base.res_bank_004"),
    ("l10n_br_base.res_bank_4", "l10n_br_base.res_bank_012"),
    ("l10n_br_base.res_bank_5", "l10n_br_base.res_bank_014"),
    ("l10n_br_base.res_bank_6", "l10n_br_base.res_bank_019"),
    ("l10n_br_base.res_bank_7", "l10n_br_base.res_bank_021"),
    ("l10n_br_base.res_bank_8", "l10n_br_base.res_bank_024"),
    ("l10n_br_base.res_bank_9", "l10n_br_base.res_bank_025"),
    ("l10n_br_base.res_bank_10", "l10n_br_base.res_bank_029"),
    ("l10n_br_base.res_bank_11", "l10n_br_base.res_bank_031"),
    ("l10n_br_base.res_bank_12", "l10n_br_base.res_bank_033"),
    ("l10n_br_base.res_bank_13", "l10n_br_base.res_bank_036"),
    ("l10n_br_base.res_bank_14", "l10n_br_base.res_bank_037"),
    ("l10n_br_base.res_bank_15", "l10n_br_base.res_bank_040"),
    ("l10n_br_base.res_bank_16", "l10n_br_base.res_bank_041"),
    ("l10n_br_base.res_bank_17", "l10n_br_base.res_bank_044"),
    ("l10n_br_base.res_bank_18", "l10n_br_base.res_bank_045"),
    ("l10n_br_base.res_bank_19", "l10n_br_base.res_bank_047"),
    ("l10n_br_base.res_bank_20", "l10n_br_base.res_bank_062"),
    ("l10n_br_base.res_bank_21", "l10n_br_base.res_bank_063"),
    ("l10n_br_base.res_bank_22", "l10n_br_base.res_bank_065"),
    ("l10n_br_base.res_bank_23", "l10n_br_base.res_bank_066"),
    ("l10n_br_base.res_bank_24", "l10n_br_base.res_bank_069"),
    ("l10n_br_base.res_bank_25", "l10n_br_base.res_bank_070"),
    ("l10n_br_base.res_bank_26", "l10n_br_base.res_bank_072"),
    ("l10n_br_base.res_bank_27", "l10n_br_base.res_bank_073"),
    ("l10n_br_base.res_bank_28", "l10n_br_base.res_bank_074"),
    ("l10n_br_base.res_bank_29", "l10n_br_base.res_bank_075"),
    ("l10n_br_base.res_bank_30", "l10n_br_base.res_bank_076"),
    ("l10n_br_base.res_bank_31", "l10n_br_base.res_bank_077"),
    ("l10n_br_base.res_bank_32", "l10n_br_base.res_bank_078"),
    ("l10n_br_base.res_bank_33", "l10n_br_base.res_bank_079"),
    ("l10n_br_base.res_bank_34", "l10n_br_base.res_bank_081"),
    ("l10n_br_base.res_bank_35", "l10n_br_base.res_bank_082"),
    ("l10n_br_base.res_bank_36", "l10n_br_base.res_bank_083"),
    ("l10n_br_base.res_bank_37", "l10n_br_base.res_bank_096"),
    ("l10n_br_base.res_bank_38", "l10n_br_base.res_bank_104"),
    ("l10n_br_base.res_bank_39", "l10n_br_base.res_bank_107"),
    ("l10n_br_base.res_bank_40", "l10n_br_base.res_bank_151"),
    ("l10n_br_base.res_bank_41", "l10n_br_base.res_bank_184"),
    ("l10n_br_base.res_bank_42", "l10n_br_base.res_bank_204"),
    ("l10n_br_base.res_bank_43", "l10n_br_base.res_bank_208"),
    ("l10n_br_base.res_bank_44", "l10n_br_base.res_bank_212"),
    ("l10n_br_base.res_bank_45", "l10n_br_base.res_bank_213"),
    ("l10n_br_base.res_bank_46", "l10n_br_base.res_bank_214"),
    ("l10n_br_base.res_bank_47", "l10n_br_base.res_bank_215"),
    ("l10n_br_base.res_bank_48", "l10n_br_base.res_bank_217"),
    ("l10n_br_base.res_bank_49", "l10n_br_base.res_bank_218"),
    ("l10n_br_base.res_bank_50", "l10n_br_base.res_bank_222"),
    ("l10n_br_base.res_bank_51", "l10n_br_base.res_bank_224"),
    ("l10n_br_base.res_bank_52", "l10n_br_base.res_bank_225"),
    ("l10n_br_base.res_bank_53", "l10n_br_base.res_bank_229"),
    ("l10n_br_base.res_bank_54", "l10n_br_base.res_bank_230"),
    ("l10n_br_base.res_bank_55", "l10n_br_base.res_bank_233"),
    ("l10n_br_base.res_bank_56", "l10n_br_base.res_bank_237"),
    ("l10n_br_base.res_bank_57", "l10n_br_base.res_bank_241"),
    ("l10n_br_base.res_bank_58", "l10n_br_base.res_bank_243"),
    ("l10n_br_base.res_bank_59", "l10n_br_base.res_bank_246"),
    ("l10n_br_base.res_bank_60", "l10n_br_base.res_bank_248"),
    ("l10n_br_base.res_bank_61", "l10n_br_base.res_bank_249"),
    ("l10n_br_base.res_bank_62", "l10n_br_base.res_bank_250"),
    ("l10n_br_base.res_bank_63", "l10n_br_base.res_bank_254"),
    ("l10n_br_base.res_bank_64", "l10n_br_base.res_bank_263"),
    ("l10n_br_base.res_bank_65", "l10n_br_base.res_bank_265"),
    ("l10n_br_base.res_bank_66", "l10n_br_base.res_bank_266"),
    ("l10n_br_base.res_bank_67", "l10n_br_base.res_bank_300"),
    ("l10n_br_base.res_bank_68", "l10n_br_base.res_bank_318"),
    ("l10n_br_base.res_bank_69", "l10n_br_base.res_bank_320"),
    ("l10n_br_base.res_bank_70", "l10n_br_base.res_bank_341"),
    ("l10n_br_base.res_bank_71", "l10n_br_base.res_bank_366"),
    ("l10n_br_base.res_bank_72", "l10n_br_base.res_bank_370"),
    ("l10n_br_base.res_bank_73", "l10n_br_base.res_bank_376"),
    ("l10n_br_base.res_bank_74", "l10n_br_base.res_bank_389"),
    ("l10n_br_base.res_bank_75", "l10n_br_base.res_bank_394"),
    ("l10n_br_base.res_bank_76", "l10n_br_base.res_bank_399"),
    ("l10n_br_base.res_bank_77", "l10n_br_base.res_bank_409"),
    ("l10n_br_base.res_bank_78", "l10n_br_base.res_bank_412"),
    ("l10n_br_base.res_bank_79", "l10n_br_base.res_bank_422"),
    ("l10n_br_base.res_bank_80", "l10n_br_base.res_bank_453"),
    ("l10n_br_base.res_bank_81", "l10n_br_base.res_bank_456"),
    ("l10n_br_base.res_bank_82", "l10n_br_base.res_bank_464"),
    ("l10n_br_base.res_bank_83", "l10n_br_base.res_bank_474"),
    ("l10n_br_base.res_bank_84", "l10n_br_base.res_bank_477"),
    ("l10n_br_base.res_bank_85", "l10n_br_base.res_bank_479"),
    ("l10n_br_base.res_bank_86", "l10n_br_base.res_bank_487"),
    ("l10n_br_base.res_bank_87", "l10n_br_base.res_bank_488"),
    ("l10n_br_base.res_bank_88", "l10n_br_base.res_bank_492"),
    ("l10n_br_base.res_bank_89", "l10n_br_base.res_bank_494"),
    ("l10n_br_base.res_bank_90", "l10n_br_base.res_bank_495"),
    ("l10n_br_base.res_bank_91", "l10n_br_base.res_bank_505"),
    ("l10n_br_base.res_bank_92", "l10n_br_base.res_bank_600"),
    ("l10n_br_base.res_bank_93", "l10n_br_base.res_bank_604"),
    ("l10n_br_base.res_bank_94", "l10n_br_base.res_bank_610"),
    ("l10n_br_base.res_bank_95", "l10n_br_base.res_bank_611"),
    ("l10n_br_base.res_bank_96", "l10n_br_base.res_bank_612"),
    ("l10n_br_base.res_bank_97", "l10n_br_base.res_bank_613"),
    ("l10n_br_base.res_bank_98", "l10n_br_base.res_bank_623"),
    ("l10n_br_base.res_bank_99", "l10n_br_base.res_bank_626"),
    ("l10n_br_base.res_bank_100", "l10n_br_base.res_bank_630"),
    ("l10n_br_base.res_bank_101", "l10n_br_base.res_bank_633"),
    ("l10n_br_base.res_bank_102", "l10n_br_base.res_bank_634"),
    ("l10n_br_base.res_bank_103", "l10n_br_base.res_bank_637"),
    ("l10n_br_base.res_bank_104", "l10n_br_base.res_bank_638"),
    ("l10n_br_base.res_bank_105", "l10n_br_base.res_bank_641"),
    ("l10n_br_base.res_bank_106", "l10n_br_base.res_bank_643"),
    ("l10n_br_base.res_bank_107", "l10n_br_base.res_bank_652"),
    ("l10n_br_base.res_bank_108", "l10n_br_base.res_bank_653"),
    ("l10n_br_base.res_bank_109", "l10n_br_base.res_bank_654"),
    ("l10n_br_base.res_bank_110", "l10n_br_base.res_bank_655"),
    ("l10n_br_base.res_bank_111", "l10n_br_base.res_bank_707"),
    ("l10n_br_base.res_bank_112", "l10n_br_base.res_bank_719"),
    ("l10n_br_base.res_bank_113", "l10n_br_base.res_bank_721"),
    ("l10n_br_base.res_bank_114", "l10n_br_base.res_bank_734"),
    ("l10n_br_base.res_bank_115", "l10n_br_base.res_bank_756"),
    ("l10n_br_base.res_bank_116", "l10n_br_base.res_bank_748"),
]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xml_ids_banks_renames)
    cr = env.cr
    cr.execute(
        """DELETE FROM ir_ui_view WHERE id IN (
        SELECT res_id FROM ir_model_data WHERE name IN (
        'view_l10n_br_base_partner_form', 'view_company_form_inherited'));
        """
    )
