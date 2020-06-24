import { InformationConfiguration } from './../basic-ui-elements/information/information-config';
import { InformationComponent } from '../basic-ui-elements/information/information.component';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SystemStatusComponent, systemInformationLabelText } from './system-status.component';
import { NO_ERRORS_SCHEMA, DebugElement, SimpleChange } from '@angular/core';
import { TestOptionComponent } from './../system-control/test-option/test-option.component';
import { SystemState } from '../system-status';
import { By } from '@angular/platform-browser';

describe('SystemStatusComponent', () => {
  let component: SystemStatusComponent;
  let fixture: ComponentFixture<SystemStatusComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SystemStatusComponent, InformationComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemStatusComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });

  it('should display "System Information" as label text', () => {
    expect(component.informationCardConfiguration.labelText).toBe('System Information');
  });

  it('should show error messages when system state is "error"', () => {
    expect(component.showError()).toBeDefined();

    let errorMsg = 'system has error';

    let errorElement = debugElement.query(By.css('.error h3'));

    if (component.showError()) {
      component.systemStatus.reason = errorMsg;

      expect(errorElement.nativeElement.textContent).toBe('system has error');
    }
  });

  it('should support hr tag', () => {
    let hrElement = debugElement.nativeElement.querySelector('hr');

    expect(hrElement).toBeTruthy();
  });

  it('should contain 2 app-card tags', async(() => {
    let cardElement = debugElement.nativeElement.querySelectorAll('app-card');

    expect(cardElement).not.toEqual(null);
    expect(cardElement.length).toEqual(2);
  }));

  it('should call method updateView when app detected change', async(() => {
    let spy = spyOn(component, 'updateView');

    component.handleServerMessage({payload: {state: SystemState.unloading}});

    expect(spy).toHaveBeenCalled();
  }));

  it('current system status is "connecting"', async(() => {
    expect(component.systemStatus.state).toBe(SystemState.connecting);
  }));

  describe('When system state is "connecting"', () => {
    it('should support heading', async(() => {
      let headingElement = debugElement.nativeElement.querySelector('app-card');
      expect(headingElement.textContent).toBe('Identifying Test System!');
    }));

    it('should display labelText "System Identification"', async(() => {
      expect(component.identifyCardConfiguration.labelText).toBe('System Identification');
    }));
  });

  describe('When system state is neither "error" nor "connecting"', () => {
    it('should contain 5 app-information tags', async(() => {

      // set system state to something different from error or connecting, i.e. to ready
      (component as any).handleServerMessage({"payload": {"state":SystemState.ready}});
      fixture.detectChanges();

      let infoElement = debugElement.nativeElement.querySelectorAll('app-information');
      expect(infoElement.length).toBe(5);
    }));

    it('should display label texts: "System", "Number of Sites", "Time", "Environment", "Handler"', async(() => {
      expect(component.infoContentCardConfiguration.labelText).toEqual('');

      // set system state to something different from error or connecting, i.e. to ready
      (component as any).handleServerMessage({"payload": {"state":SystemState.ready}});
      fixture.detectChanges();

      let lableElements = debugElement.queryAll(By.css('app-information h2'));

      let labelTexts = [];
      lableElements.forEach( l => labelTexts.push(l.nativeElement.innerText));

      expect(labelTexts).toEqual(jasmine.arrayWithExactContents(["System", "Number of Sites", "Time", "Environment", "Handler"]));

    }));

    it('should display value of system information', async(() => {
      expect(component.systemInformationConfiguration.value).toEqual('');

      // set system state to something different from error or connecting, i.e. to testing
      (component as any).handleServerMessage(
        {
          "payload":{
            "state":SystemState.testing,
            "device_id": "Test-Id",
            "env": "Test-Environment",
            "handler": "Test-Handler",
            "sites": ["Test-Site-A", "Test-Site-B"],
            "systemTime": "Test-SystemTime"
          }});
      fixture.detectChanges();

      let valueElements = debugElement.queryAll(By.css('app-information h3'));

      let valueTexts = [];
      valueElements.forEach( v => valueTexts.push(v.nativeElement.innerText));

      expect(valueTexts).toEqual(jasmine.arrayWithExactContents(["Test-Id", "Test-Environment", "Test-Handler", "Test-SystemTime"]));
    }));
  });
});
