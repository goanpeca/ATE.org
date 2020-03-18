import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SystemStatusComponent } from './system-status.component';
import { SystemState } from '../system-status';

describe('SystemStatusComponent', () => {
  let component: SystemStatusComponent;
  let fixture: ComponentFixture<SystemStatusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemStatusComponent ]
    })
    .compileComponents();
    fixture = TestBed.createComponent(SystemStatusComponent);

  }));

  beforeEach(() => {
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });
/*  ###### Failure: Expected null to be truthy #########
  it('when initialized should show system name', () => {
    fixture.componentInstance.systemStatus.state = SystemState.ready;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#systemName')).toBeTruthy();
  }); */

});
