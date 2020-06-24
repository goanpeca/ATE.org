export enum SystemState {
    connecting = 'connecting',
    error = 'error',
    initialized = 'initialized',
    loading = 'loading',
    ready = 'ready',
    testing = 'testing',
    paused = 'paused',
    unloading = 'unloading'
}

export class SystemStatus {

    deviceId: string;
    env: string;
    handler: string;
    time: string;
    sites: Array<string>;
    program: string;
    log: string;
    state: SystemState;
    reason: string;

    constructor() {
        this.deviceId = 'invalid';
        this.env = 'invalid';
        this.handler = 'invalid';
        this.time = 'invalid',
        this.sites = [],
        this.program = 'connecting',
        this.log = 'connecting',
        this.state = SystemState.connecting;
        this.reason = 'invalid error';
    }

    update(json) {

        if (json.device_id && this.deviceId !== json.device_id) {
            this.deviceId = json.device_id;
        }

        if (json.env && this.env !== json.env) {
            this.env = json.env;
        }

        if (json.handler && this.handler !== json.handler) {
            this.handler = json.handler;
        }

        if (json.systemTime && json.systemTime !== this.time) {
            this.time = json.systemTime;
        }

        if (json.sites) {
            this.sites = json.sites;
        }

        if (json.program ) {
            this.program  = json.program;
        }

        if (json.log) {
            this.log = json.log;
        }

        if (json.state && json.state !== this.state) {
            this.state = json.state;
        }

        if (json.error_message && json.error_message !== this.reason) {
            this.reason = json.error_message;
        }
   }
}
