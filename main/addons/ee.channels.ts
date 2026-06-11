// CUSTOM: EE addon IPC channel names — addon-owned so core IPC_ACTIONS stays untouched
export const EE_CHANNELS = {
  detectArelle: 'ee:detect-arelle',
  detectTaxonomy: 'ee:detect-taxonomy',
  validateXbrl: 'ee:validate-xbrl',
} as const;
