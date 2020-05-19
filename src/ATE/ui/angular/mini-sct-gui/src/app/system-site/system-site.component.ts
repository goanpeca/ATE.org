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

  sitesControl: ISite[] = [];
  sitesTest: ISite[] = [];

// sitesObj
  sitesObj = { Control: this.sitesControl,
              TestApp: this.sitesTest
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
    const topicSplit: string[] = topic.split('/');
    const site: string = topicSplit[topicSplit.length - 1];

    // we ignore master status, it will be handled somewehere else
    if (topic.includes('Master')) { return; }

    if (topic.includes('site')) {
      const siteNum = site.replace(/^\D+/g, '');
      const siteType = topicSplit[2];
      if (this.sites.find(x => x === siteNum)) {
          let singleSite: ISite;
          singleSite = {
            type: topicSplit[2],
            siteId: siteNum,
            state: payload.state
          };

          const s: ISite[] = this.sitesObj[siteType];
          const num = s.findIndex(x => x.siteId === siteNum);
          if (num !== -1) {
            this.sitesObj[siteType][num] = singleSite;
            return;
          }

          this.sitesObj[siteType].push(singleSite);
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

export interface ISite {
  type: string;
  siteId: string;
  state: string;
}
