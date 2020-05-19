import { ButtonComponent } from './../../basic-ui-elements/button/button.component';
import { async, ComponentFixture, TestBed, ComponentFixtureNoNgZone } from '@angular/core/testing';
import { TestExecutionComponent } from './test-execution.component';
import { DebugElement, NO_ERRORS_SCHEMA } from '@angular/core';
import { By } from '@angular/platform-browser';
import { SystemState } from 'src/app/system-status';


describe('TestExecutionComponent', () => {
  let component: TestExecutionComponent;
  let fixture: ComponentFixture<TestExecutionComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestExecutionComponent, ButtonComponent ],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestExecutionComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create test-execution component', () => {
    expect(component).toBeTruthy();
  });

  it('should support label text "Test Execution"', () => {
    const cardLabelText = 'Test Execution';

    expect(component.testExecutionControlCardConfiguration.labelText).toBe(cardLabelText, 'Should be "Test Execution"');
  });

  it('should show a start Dut-Test button', () => {
    const buttonText = 'Start DUT-Test';

    expect(component.startDutTestButtonConfig.labelText).toBe(buttonText, 'Should be "Start DUT-Test"');
  });

  it('should have a disabled button if system state is "connecting"', () => {
    let btnElement = debugElement.nativeElement.querySelectorAll('app-button');

    expect(btnElement.length).toBe(1);

    let systemState = component.systemStatus.state === SystemState.connecting;

    if (systemState) {
      expect(btnElement[0].hasAttribute('disabled')).toBe(false, 'start DUT-Test button is expected to be disabled');
    }
  });

  describe('When system state is "ready"', () => {
    it('button should be active', async(() => {
      let btnElement = debugElement.nativeElement.querySelector('app-button');
      expect(btnElement).toBeDefined();

      let systemState = component.systemStatus.state === SystemState.ready;

      if (systemState) {
        fixture.detectChanges();
        expect(btnElement.hasAttribute('disabled')).toBe(false, 'start DUT-Test button is expected to be active');
      }
    }));

    it('should call method startDutTestButtonClicked when button clicked', async(() => {
      let spy = spyOn(component, 'startDutTestButtonClicked').and.callThrough();

      expect(spy).toHaveBeenCalledTimes(0);

      let btnElement = debugElement.nativeElement.querySelector('app-button');
      let systemState = component.systemStatus.state === SystemState.ready;

      if (systemState) {
        btnElement.click();
        fixture.detectChanges();

        expect(spy).toHaveBeenCalled();
      }
    }));
  });
});
