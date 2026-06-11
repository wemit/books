// CUSTOM: aggregated addon preload surface, spread into `ipc` in main/preload.ts
import { eePreload } from './ee.preload';

export const mainAddonPreload = {
  ee: eePreload,
} as const;
