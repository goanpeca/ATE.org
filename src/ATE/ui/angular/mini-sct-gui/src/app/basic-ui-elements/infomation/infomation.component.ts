import { Component, OnInit, Input } from '@angular/core';
import { InformationConfiguration } from './information-config';

@Component({
  selector: 'app-infomation',
  templateUrl: './infomation.component.html',
  styleUrls: ['./infomation.component.scss']
})
export class InfomationComponent implements OnInit {
  @Input() informationConfig: InformationConfiguration;

  constructor() {
    this.informationConfig = new InformationConfiguration();
   }

  ngOnInit() {
  }

  typeOf(value: any) {
    value = this.informationConfig.value;
    return typeof(value);
  }
}
