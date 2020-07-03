import { ButtonComponent } from './../../basic-ui-elements/button/button.component';
import { async, ComponentFixture, TestBed, ComponentFixtureNoNgZone } from '@angular/core/testing';
import { TestExecutionComponent } from './test-execution.component';
import { DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';
import { SystemState } from 'src/app/system-status';
import { CardComponent } from 'src/app/basic-ui-elements/card/card.component';


describe('TestExecutionComponent', () => {
  let component: TestExecutionComponent;
  let fixture: ComponentFixture<TestExecutionComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestExecutionComponent, ButtonComponent, CardComponent ],
      schemas: []
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

  describe('When system state is "connecting"', () => {
    it('should have a disabled start-dut-test-button', () => {

      // connecting
      (component as any).handleServerMessage({payload: {state: SystemState.connecting}});
      fixture.detectChanges();

      let startDutTestButton = debugElement.queryAll(By.css('app-button'))
                                .filter(b => b.nativeElement.innerText === 'Start DUT-Test')[0]
                                  .nativeElement.querySelector('button');

      expect(startDutTestButton.hasAttribute('disabled'))
        .toBeTruthy('start DUT-Test button is expected to be inactive');
    });
  });

  describe('When system state is "ready"', () => {
    it('start-dut-test-button should be active', async(() => {

      // ready state
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();

      let startDutTestButton = debugElement.queryAll(By.css('app-button'))
                                .filter(b => b.nativeElement.innerText === 'Start DUT-Test')[0]
                                  .nativeElement.querySelector('button');

      expect(startDutTestButton.hasAttribute('disabled'))
        .toBeFalsy('start DUT-Test button is expected to be active');
    }));

    it('should call method startDutTestButtonClicked when button clicked', async(() => {

      // ready state
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();

      let spy = spyOn(component, 'startDutTest').and.callThrough();
      expect(spy).toHaveBeenCalledTimes(0);

      let startDutTestButton = debugElement.queryAll(By.css('app-button'))
                                 .filter(b => b.nativeElement.innerText === 'Start DUT-Test')[0]
                                  .nativeElement.querySelector('button');

      startDutTestButton.click();
      fixture.detectChanges();
      expect(spy).toHaveBeenCalled();
    }));
  });
});
