import { InformationConfiguration } from './../basic-ui-elements/infomation/information-config';
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
      declarations: [ SystemStatusComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SystemStatusComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges(); // initial binding
  });

  it('should create status component', () => {
    expect(component).toBeTruthy();
  });

  it('should display "System Information" as label text', () => {
    expect(component.informationCardConfiguration.labelText).toBe('System Information');
  });

  it('should show error messages when system state is "error"', () => {
    let errorMsg = 'system error';

    let errorElement = debugElement.query(By.css('.error h3'));

    if (component.systemStatus.state === SystemState.error) {
      errorMsg = component.systemStatus.reason;

      expect(errorElement.nativeElement.textContent).toEqual('system error');
      expect(component.visiable).toBe(true);
    } else {
      component.visiable = false;

      expect(component.visiable).toBe(false);
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

    component.ngOnChanges();
    fixture.detectChanges();

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
    it('should contain 5 app-infomation tags', async(() => {
      let infoElement = debugElement.nativeElement.querySelectorAll('app-infomation');
      let systemState = component.systemStatus.state !== SystemState.error && component.systemStatus.state !== SystemState.connecting;

      if (systemState) {
        expect(infoElement).not.toEqual(null);
        expect(infoElement.length).toBe(5);
      } else {
        expect(infoElement.length).toBe(0);
      }
    }));

    it('should display labelText', async(() => {
      expect(component.infoContentCardConfiguration.labelText).toEqual('');

      let infoElement = debugElement.nativeElement.querySelectorAll('app-infomation');
      let systemState = component.systemStatus.state !== SystemState.error && component.systemStatus.state !== SystemState.connecting;

      if (systemState) {
        expect(infoElement[0]).toBe('System');
        expect(infoElement[0]).toEqual(component.sytemInformationConfiguration.labelText);
        expect(infoElement[1]).toBe('Number of Sites');
        expect(infoElement[1]).toEqual(component.numberOfSitesConfiguration.labelText);

        expect(infoElement[2]).toBe('Time');
        expect(infoElement[2]).toEqual(component.timeInformationConfiguration.labelText);

        expect(infoElement[3]).toBe('Environment');
        expect(infoElement[3]).toEqual(component.environmentInformationConfiguration.labelText);

        expect(infoElement[4]).toBe('Handler');
        expect(infoElement[4]).toEqual(component.handlerInformationConfiguration.labelText);
      }
    }));

    it('should display value of system information', async(() => {
      expect(component.sytemInformationConfiguration.value).toEqual('');

      let infoElement = debugElement.nativeElement.querySelectorAll('app-infomation');
      let systemState = component.systemStatus.state !== SystemState.error && component.systemStatus.state !== SystemState.connecting;

      if (systemState) {
      expect(infoElement[0]).toBe('invalid');
      expect(infoElement[0]).toEqual(component.sytemInformationConfiguration.value);
      expect(infoElement[1]).toBe(0);
      expect(infoElement[1]).toEqual(component.numberOfSitesConfiguration.value);

      expect(infoElement[2]).toBe('invalid');
      expect(infoElement[2]).toEqual(component.timeInformationConfiguration.value);

      expect(infoElement[3]).toBe('invalid');
      expect(infoElement[3]).toEqual(component.environmentInformationConfiguration.value);

      expect(infoElement[4]).toBe('invalid');
      expect(infoElement[4]).toEqual(component.handlerInformationConfiguration.value);
    }
    }));
  });

});
