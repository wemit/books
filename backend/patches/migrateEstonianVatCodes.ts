import { DatabaseManager } from '../database/manager';

/**
 * EE: lhvVatCode -> vatCode, lhvArchivalId -> archivalId, legacy rows ->
 * importBank 'lhv', and ZERO_EU_B2B -> ZERO_EU_GOODS. New columns are created
 * by the schema sync that runs before patches; old columns are left unused.
 */
async function execute(dm: DatabaseManager) {
  const knex = dm.db?.knex;
  if (!knex) {
    return;
  }

  const hasNewVat = await knex.schema.hasColumn('JournalEntry', 'vatCode');
  const hasNewArch = await knex.schema.hasColumn('JournalEntry', 'archivalId');
  const hasImportBank = await knex.schema.hasColumn(
    'JournalEntry',
    'importBank'
  );
  const hasOldVat = await knex.schema.hasColumn('JournalEntry', 'lhvVatCode');
  const hasOldArch = await knex.schema.hasColumn(
    'JournalEntry',
    'lhvArchivalId'
  );

  if (hasNewVat && hasOldVat) {
    await knex('JournalEntry')
      .whereNotNull('lhvVatCode')
      .whereRaw("(vatCode IS NULL OR vatCode = '')")
      .update({ vatCode: knex.ref('lhvVatCode') });
  }

  if (hasNewArch && hasOldArch) {
    await knex('JournalEntry')
      .whereNotNull('lhvArchivalId')
      .whereRaw("(archivalId IS NULL OR archivalId = '')")
      .update({ archivalId: knex.ref('lhvArchivalId') });

    // EE: legacy imports were LHV-only — stamp source bank so pair-dedup works
    if (hasImportBank) {
      await knex('JournalEntry')
        .whereNotNull('lhvArchivalId')
        .whereRaw("(importBank IS NULL OR importBank = '')")
        .update({ importBank: 'lhv' });
    }
  }

  if (hasNewVat) {
    await knex('JournalEntry')
      .where({ vatCode: 'ZERO_EU_B2B' })
      .update({ vatCode: 'ZERO_EU_GOODS' });
  }
}

export default { execute };
