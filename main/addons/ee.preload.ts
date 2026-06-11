// CUSTOM: EE addon preload IPC surface, exposed as ipc.ee
import { ipcRenderer } from 'electron';
import type { BackendResponse } from 'utils/ipc/types';
// CUSTOM: type-only — keeps node-bound arelleValidator out of the preload bundle
import type { ValidateOptions } from '../arelleValidator';
import { EE_CHANNELS } from './ee.channels';

export const eePreload = {
  async detectArelle(arellePath: string): Promise<string | null> {
    return (await ipcRenderer.invoke(EE_CHANNELS.detectArelle, arellePath)) as
      | string
      | null;
  },

  async detectTaxonomy(): Promise<string | null> {
    return (await ipcRenderer.invoke(EE_CHANNELS.detectTaxonomy)) as
      | string
      | null;
  },

  async validateXbrl(options: ValidateOptions): Promise<BackendResponse> {
    return (await ipcRenderer.invoke(
      EE_CHANNELS.validateXbrl,
      options
    )) as BackendResponse;
  },
};
