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
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('when initialized should show system name', () => {
    const fixture = TestBed.createComponent(SystemStatusComponent);
    fixture.componentInstance.systemStatus.state = SystemState.ready;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#systemName')).toBeTruthy();
  });

});
