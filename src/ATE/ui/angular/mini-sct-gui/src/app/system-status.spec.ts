import { SystemStatus } from './system-status';

describe('SystemStatus', () => {
  let systemStatus: SystemStatus;

  beforeEach(() => {
    systemStatus = new SystemStatus();
  });

  it('should create an instance', () => {
    expect(systemStatus).toBeTruthy();
  });

  it('should expose a update() method', () => {
    expect(typeof systemStatus.update).toEqual('function');
  });

  it('should create a string value', () => {
    const handler = 'KLA-Prober';
    expect(typeof systemStatus.handler).toEqual('string');
  });
});
