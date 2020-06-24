import { ButtonConfiguration } from 'src/app/basic-ui-elements/button/button-config';
import { InputConfiguration } from './../../basic-ui-elements/input/input-config';
import { ButtonComponent } from './../../basic-ui-elements/button/button.component';
import { async, ComponentFixture, TestBed, tick } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA, DebugElement, Component, OnChanges, Input } from '@angular/core';
import { TestOptionComponent, TestOptionValue, TestOption } from './test-option.component';
import { By } from '@angular/platform-browser';
import { SystemState } from 'src/app/system-status';
import { createUrlResolverWithoutPackagePrefix } from '@angular/compiler';
import { toBase64String } from '@angular/compiler/src/output/source_map';
import { CheckboxComponent } from 'src/app/basic-ui-elements/checkbox/checkbox.component';
import { InputComponent } from 'src/app/basic-ui-elements/input/input.component';

describe('TestOptionComponent', () => {
  let component: TestOptionComponent;
  let fixture: ComponentFixture<TestOptionComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestOptionComponent, ButtonComponent, CheckboxComponent, InputComponent ],
      schemas: [ NO_ERRORS_SCHEMA ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestOptionComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create test-option component', () => {
    expect(component).toBeTruthy();
  });

  it('should create instance of TestOptionValue', () => {
    expect(new TestOptionValue()).toBeTruthy();
  });

  it('should create instance of TestOption', () => {
    let name = 'Test Name';
    expect(new TestOption(name)).toBeTruthy();
    expect (new TestOption(name).name).toBe(name);
  });

  describe('Class TestOption', () => {
    it('should change values from onChange() when checked element is true ', () => {
      let testOption = new TestOption('Test');
      let checked = true;
      testOption.onChange(checked);

      expect(testOption.toBeAppliedValue.active).toBe(true);
      expect(testOption.inputConfig.disabled).toBe(false);
    });

    it('should get true value from haveToApply() when some change occured', () => {
      let testOption = new TestOption('Test');
      let anyChanges = false;
      if (testOption.toBeAppliedValue.active !== testOption.currentValue.active) {
        anyChanges = true;
      }

      expect(testOption.haveToApply()).toEqual(anyChanges);
    });

  });

  it('should show Apply- and Reset-button', () => {
    const buttonText = ['Apply', 'Reset'];

    expect(component.applyTestOptionButtonConfig.labelText).toBe(buttonText[0], 'Should be "Apply"');
    expect(component.resetOptionButtonConfig.labelText).toBe(buttonText[1], 'Should be "Reset"');
  });

  it('should show 6 test options', () => {
    const testOptions = ['Stop on Fail', 'Single Step', 'Stop at Test Number', 'Trigger For Test Number', 'Trigger On Failure', 'Trigger Site Specific'];

    expect(component.testOptions.length).toBe(6, 'Should have 6 test options');
  });

  it('should call method resetTestOptions when reset button clicked', async(() => {

    // ready
    (component as any).handleServerMessage({"payload": {"state":SystemState.ready}});
    fixture.detectChanges();

    let checkboxes = fixture.debugElement.queryAll(By.css('app-checkbox'));
    let checkbox = checkboxes.filter(e => e.nativeElement.innerText === "Stop on Fail")[0].nativeElement.querySelector('.slider');

    checkbox.click();
    fixture.detectChanges();

    let buttons = fixture.debugElement.queryAll(By.css('app-button'));
    let resetButton = buttons.filter(e => e.nativeElement.innerText === "Reset")[0].nativeElement.querySelector('button');
    
    let spy = spyOn(component, 'resetTestOptions');
    resetButton.click();
    fixture.detectChanges();

    expect(spy).toHaveBeenCalled();
  }));

  describe('Tags of the other component type', () => {
    it('should contain an app-card tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-card');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-button tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-button');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-input tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-input');
      expect(componentElement).not.toEqual(null);
    }));

    it('should contain an app-checkbox tag', async(() => {
      let componentElement = debugElement.nativeElement.querySelector('app-checkbox');
      expect(componentElement).not.toEqual(null);
    }));
  });

  describe('Option: Stop-On-Fail', () => {
    it('should display "Stop on Fail"', async(() => {
      expect(component.stopOnFailOption.checkboxConfig.labelText).toContain('Stop on Fail');
    }));

    it('should be disabled when system initialized', async(() => {
      let testOption = new TestOption('stop_on_fail');

      testOption.currentValue.active = component.stopOnFailOption.checkboxConfig.disabled;
      fixture.detectChanges();

      expect(testOption.currentValue.active).toBe(true);
    }));

    it('should be active only when system state is ready', async(() => {

      // set ready
      (component as any).handleServerMessage({"payload": {"state":SystemState.ready}});
      fixture.detectChanges();

      let checkboxes = fixture.debugElement.queryAll(By.css('app-checkbox'));
      let checkbox = checkboxes.filter(e => e.nativeElement.innerText === "Stop on Fail")[0].nativeElement.querySelector('input');

      expect(checkbox.hasAttribute('disabled')).toBeFalsy();
    }));

    it('should call sendOptionsToServer method when apply button clicked', async(() => {

      // ready
      (component as any).handleServerMessage({"payload": {"state":SystemState.ready}});
      fixture.detectChanges();

      let checkboxes = fixture.debugElement.queryAll(By.css('app-checkbox'));
      let checkbox = checkboxes.filter(e => e.nativeElement.innerText === "Stop on Fail")[0].nativeElement.querySelector('.slider');

      checkbox.click();
      fixture.detectChanges();

      let buttons = fixture.debugElement.queryAll(By.css('app-button'));
      let applyButton = buttons.filter(e => e.nativeElement.innerText === "Apply")[0].nativeElement.querySelector('button');
    
      let spy = spyOn(component, 'sendOptionsToServer');
      applyButton.click();

      fixture.detectChanges();
      expect(spy).toHaveBeenCalled();
    }));
  });
});
