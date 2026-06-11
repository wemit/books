// CUSTOM: registers main-process addon IPC handlers; called once from core
import { registerEeHandlers } from './ee.handlers';

export function registerMainAddonHandlers() {
  registerEeHandlers();
}
