import { Component, OnInit, Input } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';

@Component({
  selector: 'app-system-status',
  templateUrl: './system-status.component.html',
  styleUrls: ['./system-status.component.scss']
})
export class SystemStatusComponent implements OnInit {

  @Input() systemStatus: SystemStatus = new SystemStatus();

  protected mySystemState = SystemState;
  // property for error information
  visiable = true;

  constructor() { }

  ngOnInit() {
  }
}
