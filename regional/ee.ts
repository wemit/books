export type VatCodeName =
  | 'EE24'
  | 'EE13'
  | 'EE9'
  | 'EE0'
  | 'EU_RC_GOODS'
  | 'EU_RC_SERVICES'
  | 'NON_EU_RC'
  | 'ZERO_EU_B2B'
  | 'ZERO_EU_GOODS'
  | 'ZERO_EU_SERVICES'
  | 'ZERO_EU_TRIANGLE'
  | 'ZERO_EXPORT'
  | 'EXEMPT'
  | 'MARGIN_24'
  | 'MARGIN_22'
  | 'MARGIN_9'
  | 'MARGIN_5'
  | 'OSS_SALES'
  | 'EU_FIXED_ESTAB';

export interface VatCodeSpec {
  rate: number;
  reverseCharge: boolean;
  description: string;
  specialScheme?: 'margin' | 'oss' | 'fixedEstablishment';
}

export const VAT_CODES: Record<VatCodeName, VatCodeSpec> = {
  EE24: {
    rate: 24,
    reverseCharge: false,
    description: 'Estonian standard rate 24%',
  },
  EE13: {
    rate: 13,
    reverseCharge: false,
    description: 'Estonian reduced rate 13% (accommodation)',
  },
  EE9: {
    rate: 9,
    reverseCharge: false,
    description: 'Estonian reduced rate 9% (books, medicines)',
  },
  EE0: { rate: 0, reverseCharge: false, description: 'Estonian zero-rated' },
  EU_RC_GOODS: {
    rate: 24,
    reverseCharge: true,
    description: 'EU acquisition of goods (reverse charge)',
  },
  EU_RC_SERVICES: {
    rate: 24,
    reverseCharge: true,
    description: 'EU service import (reverse charge)',
  },
  NON_EU_RC: {
    rate: 24,
    reverseCharge: true,
    description: 'Non-EU service import (reverse charge)',
  },
  ZERO_EU_B2B: {
    rate: 0,
    reverseCharge: false,
    description: 'EU B2B sale — goods (deprecated, use ZERO_EU_GOODS)',
  },
  ZERO_EU_GOODS: {
    rate: 0,
    reverseCharge: false,
    description:
      'EU B2B supply of goods (zero-rated; KMD 3.1 + 3.1.1, VD goods)',
  },
  ZERO_EU_SERVICES: {
    rate: 0,
    reverseCharge: false,
    description: 'EU B2B supply of services (zero-rated; KMD 3.1, VD services)',
  },
  ZERO_EU_TRIANGLE: {
    rate: 0,
    reverseCharge: false,
    description:
      'EU triangular resale as intermediary (VD triangular column only, not on KMD)',
  },
  ZERO_EXPORT: {
    rate: 0,
    reverseCharge: false,
    description: 'Export outside EU (zero-rated)',
  },
  EXEMPT: { rate: 0, reverseCharge: false, description: 'VAT exempt' },
  MARGIN_24: {
    rate: 24,
    reverseCharge: false,
    specialScheme: 'margin',
    description:
      'Margin scheme 24% — used goods/art/antiques (KMS §41,42; KMD line 1, INF erikord)',
  },
  MARGIN_22: {
    rate: 22,
    reverseCharge: false,
    specialScheme: 'margin',
    description:
      'Margin scheme 22% — historical (2024-01..2025-06; KMD line 12)',
  },
  MARGIN_9: {
    rate: 9,
    reverseCharge: false,
    specialScheme: 'margin',
    description:
      'Margin scheme 9% — used goods/art/antiques (KMS §41,42; KMD line 2)',
  },
  MARGIN_5: {
    rate: 5,
    reverseCharge: false,
    specialScheme: 'margin',
    description:
      'Margin scheme 5% — historical press rate (~2022-08..2025-06; KMD line 2¹)',
  },
  OSS_SALES: {
    rate: 0,
    reverseCharge: false,
    specialScheme: 'oss',
    description:
      'OSS / digital services to EU consumers (§43) — declared on the separate OSS return, not on KMD. Actual rate is per destination country.',
  },
  EU_FIXED_ESTAB: {
    rate: 0,
    reverseCharge: false,
    specialScheme: 'fixedEstablishment',
    description:
      'Supply via an EU permanent establishment — taxed in that country at its rate, not Estonian turnover (off KMD).',
  },
};

export const EE_COUNTIES = [
  'Harju',
  'Hiiu',
  'Ida-Viru',
  'Jõgeva',
  'Järva',
  'Lääne',
  'Lääne-Viru',
  'Põlva',
  'Pärnu',
  'Rapla',
  'Saare',
  'Tartu',
  'Valga',
  'Viljandi',
  'Võru',
] as const;

export type EeCounty = typeof EE_COUNTIES[number];

export const EE_VAT_NUMBER_RE = /^EE\d{9}$/;
export const EE_REGISTRY_CODE_RE = /^\d{8}$/;
