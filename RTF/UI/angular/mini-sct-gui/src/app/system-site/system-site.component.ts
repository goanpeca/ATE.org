import { Component, OnInit, Input, Pipe, PipeTransform } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';

@Component({
  selector: 'app-system-site',
  templateUrl: './system-site.component.html',
  styleUrls: ['./system-site.component.scss']
})

@Pipe({
  name: 'retrieveData',
  pure: true
})
export class SystemSiteComponent implements OnInit, PipeTransform {

  constructor() { }

  @Input() msg: JSON;
  @Input() sites: string[];
  @Input() systemStatus: SystemStatus = new SystemStatus();
  mySystemState = SystemState;

  _sites_control: Site[] = [];
  _sites_test: Site[] = [];


  _sites_ = { Control: this._sites_control,
              TestApp: this._sites_test
            };
  transform(value: JSON, args?: any): any {
    return this.retrieveData(value);
  }

  retrieveData(message) {
    if (!message) { return; }
    const jsonMessage = message.payload;
    const payload = JSON.parse(jsonMessage);
    const topic = message.topic;

    if (payload.type !== 'status') {
      return;
    }

    this.getMessageinfos(topic, payload);
  }

  getMessageinfos(topic: string, payload) {
    const source = '';
    const topic_split: string[] = topic.split('/');
    const site: string = topic_split[topic_split.length - 1];

    // we ignore master status, it will be handled somewehere else
    if (topic.includes('Master')) { return; }

    if (topic.includes('site')) {
      const site_num = site.replace(/^\D+/g, '');
      const _type = topic_split[2];
      if (this.sites.find(x => x === site_num)) {
          let _site: Site;
          _site = {
            type: topic_split[2],
            site_id: site_num,
            state: payload.state
          };

          let _s: Site[] = this._sites_[_type];
          const num = _s.findIndex(x => x.site_id === site_num);
          if (num !== -1) {
            this._sites_[_type][num] = _site;
            return;
          }

          this._sites_[_type].push(_site);
        }
    }

    return source;
  }

  ngOnInit() {}
}

export enum SourceApp {
  Master = 'master',
  Control = 'control',
  Test = 'test',

}


export interface Site {
  type: string;
  site_id: string;
  state: string;
}
