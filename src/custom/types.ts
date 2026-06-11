// CUSTOM: renderer addon contract — app-level contributions only; country
// data stays on upstream's native regional system
import type { Fyo } from 'fyo';
import type { Report } from 'reports/Report';
import type { RouteRecordRaw } from 'vue-router';
import type { SidebarRoot } from 'src/utils/types';

export type ReportClass = (new (fyo: Fyo) => Report) & {
  title: string;
  reportName: string;
  isInventory: boolean;
};

export interface AppAddon {
  name: string;
  condition?: (fyo: Fyo) => boolean;
  reports?: Record<string, ReportClass>;
  routes?: RouteRecordRaw[];
  sidebar?: (fyo: Fyo) => SidebarRoot[];
  listActions?: Record<string, AddonListAction[]>;
}

export interface AddonListAction {
  label: string;
  action: (fyo: Fyo) => unknown | Promise<unknown>;
}
