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

  constructor() {
    this.systemStatus = new SystemStatus();
  }

  @Input() msg: JSON;
  @Input() sites: string[];
  @Input() systemStatus: SystemStatus;
  mySystemState = SystemState;

  sitesControl: Site[] = [];
  siteTest: Site[] = [];

  _SITES = {
    Control: this.sitesControl,
    TestApp: this.siteTest
  };

  transform(value: JSON, args) {
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
    const topicSplit: string[] = topic.split('/');
    const site: string = topicSplit[topicSplit.length - 1];

    // we ignore master status, it will be handled somewehere else
    if (topic.includes('Master')) { return; }

    if (topic.includes('site')) {
      const siteNum = site.replace(/^\D+/g, '');
      const type = topicSplit[2];
      if (this.sites.find(x => x === siteNum)) {
        let site1: Site;
        site1 = {
          type: topicSplit[2],
          siteId: siteNum,
          state: payload.state
        };

        const SITE_LIST: Site[] = this._SITES[type];
        const num = SITE_LIST.findIndex(x => x.siteId === siteNum);
        if (num !== -1) {
          this._SITES[type][num] = site1;
          return;
        }

        this._SITES[type].push(site1);
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
  siteId: string;
  state: string;
}
