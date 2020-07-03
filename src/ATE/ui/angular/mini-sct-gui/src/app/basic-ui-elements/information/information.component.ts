import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { InformationConfiguration } from './information-config';

@Component({
  selector: 'app-information',
  templateUrl: './information.component.html',
  styleUrls: ['./information.component.scss']
})
export class InformationComponent implements OnInit, OnChanges {
  @Input() informationConfig: InformationConfiguration;

  constructor() {
    this.informationConfig = new InformationConfiguration();
   }

  ngOnInit() {
  }

  ngOnChanges() {
    console.log('Information component detected change');
  }

  typeOf(value: any) {
    value = this.informationConfig.value;
    return typeof(value);
  }
}
