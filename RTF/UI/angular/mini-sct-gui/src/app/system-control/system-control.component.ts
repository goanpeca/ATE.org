import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';
import { SystemStatus, SystemState } from '../system-status';

@Component({
  selector: 'app-system-control',
  templateUrl: './system-control.component.html',
  styleUrls: ['./system-control.component.scss']
})

export class SystemControlComponent {

  mySystemState = SystemState;

  @Input() systemStatus: SystemStatus = new SystemStatus();
  @Output() startDutTestEvent: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() unLoadTestProgramEvent: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() lotNumber: EventEmitter<string> = new EventEmitter<string>();

  constructor() {
  }

  startDutTest() {
    this.startDutTestEvent.emit(true);
  }

  unLoadTestProgram() {
    this.unLoadTestProgramEvent.emit(true);
  }

  sendLotNumber(lotNumber: string) {
    this.lotNumber.emit(lotNumber);
  }
  // TODO: function musst be refined later
  unloadLotNumber() {
    this.lotNumber.emit(null);
  }
  // check input
  numericOnly(event): boolean {
    // TODO: There must be more possibilities hier for testing purpose ??
    // allows only number and .
    const pattern = /^([0-9.])$/;
    const result = pattern.test(event.key);
    return result;
  }
}
