export enum SystemState {
    connecting = "connecting",
    error = "error",
    initialized = "initialized",
    loading = "loading",
    ready = "ready",
    testing = "testing",
    paused = "paused",
    unloading = "unloading"
}

export class SystemStatus {
    
    device_id : string
    env : string
    handler : string
    time : string
    sites : string[];
    program : string
    log : string
    state : SystemState
    reason: string

    constructor()
    {
        this.device_id = "invalid"
        this.env = "invalid"
        this.handler = "invalid"
        this.time = "invalid",
        this.sites = [],
        this.program = "connecting",
        this.log = "connecting",
        this.state = SystemState.connecting
        this.reason = "invalid error"
    }

    update(json)
    {
        if (json.device_id)
        {
            this.device_id = json.device_id
        }

        if (json.env)
        {
            this.env = json.env
        }

        if (json.handler)
        {
            this.handler = json.handler
        }

        if (json.systemTime)
        {
            this.time = json.systemTime
        }

        if (json.sites)
        {
            this.sites = json.sites
        }

        if (json.program )
        {
            this.program  = json.program 
        }

        if (json.log)
        {
            this.log = json.log
        }

        if (json.state)
        {
            this.state = json.state
        }
   }
}
