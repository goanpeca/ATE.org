import { InputComponent } from './../../basic-ui-elements/input/input.component';
import { ButtonComponent } from './../../basic-ui-elements/button/button.component';
import { CardConfiguration } from 'src/app/basic-ui-elements/card/card.component';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { LotHandlingComponent } from './lot-handling.component';
import { DebugElement, NO_ERRORS_SCHEMA } from '@angular/core';
import { By } from '@angular/platform-browser';
import { SystemState } from 'src/app/system-status';

describe('LotHandlingComponent', () => {
  let component: LotHandlingComponent;
  let fixture: ComponentFixture<LotHandlingComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LotHandlingComponent, ButtonComponent, InputComponent],
      schemas: [NO_ERRORS_SCHEMA]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LotHandlingComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
  });

  it('should create lot-handling component', () => {
    expect(component).toBeTruthy();
  });

  it('should have header text for card element', () => {
    const cardLabelText = 'Lot Handling';
    fixture.detectChanges();

    const card = debugElement.query(By.css('app-card'));

    expect(component.lotCardConfiguration.labelText).toBe(cardLabelText, 'Should be "Lot Handling"');
  });

  it('should show a load lot button', () => {
    const loadButton = debugElement.query(By.css('.inputButton app-button'));

    expect(loadButton.nativeElement.textContent.trim()).toBe('Load Lot');
  });

  it('should show an unload lot button', () => {
    const unLoadButton = debugElement.query(By.css('.unloadLotBtn app-button'));

    expect(unLoadButton.nativeElement.textContent.trim()).toBe('Unload Lot');
  });

  it('should show input field for lot number', () => {
    const input = debugElement.query(By.css('.inputButton app-input'));

    expect(input.nativeElement).toBeDefined();
  });

  it('should display error message', async(() => {
    const inputElement = debugElement.nativeElement.querySelector('.inputButton app-input');
    component.lotNumberInputConfig.value = '1234';

    component.sendLotNumber();
    fixture.detectChanges();

    expect(inputElement.textContent).toBe('A lot number should be in 6.3 format like \"123456.123\"');
  }));

  it('buttons should be disabled', () => {
    let btnElement = debugElement.nativeElement.querySelectorAll('app-button');

    expect(btnElement.length).toBe(2);

    let systemState = component.systemStatus.state === SystemState.connecting;

    if (systemState) {
      expect(btnElement[0].hasAttribute('disabled')).toBe(false, 'load lot button is expected to be disabled');
      expect(btnElement[1].hasAttribute('disabled')).toBe(false, 'unload lot button is expected to be disabled');
    }
  });

  it('should call method sendLotNumber when button clicked', async(() => {
    let spy = spyOn(component, 'sendLotNumber');

    component.loadLot();
    fixture.detectChanges();

    expect(spy).toHaveBeenCalled();
  }));

  describe('When system state is "ready"', () => {
    it('unload lot button should be active', async(() => {
      let btnElement = debugElement.nativeElement.querySelectorAll('app-button');

      expect(btnElement.length).toBe(2);

      let systemState = component.systemStatus.state === SystemState.ready;

      if (systemState) {
        expect(btnElement[0].hasAttribute('disabled')).toBe(true, 'load lot button is expected to be disabled');
        expect(btnElement[1].hasAttribute('disabled')).toBe(false, 'unload lot button is expected to be active');
      }
    }));

    it('should call method unloadLotButtonClicked when button clicked', async(() => {
      let spy = spyOn(component, 'unloadLot').and.callThrough();

      expect(spy).toHaveBeenCalledTimes(0);

      let btnElement = debugElement.nativeElement.querySelectorAll('app-button');
      let systemState = component.systemStatus.state === SystemState.ready;

      if (systemState) {
        btnElement[1].click();
        fixture.detectChanges();

        expect(spy).toHaveBeenCalled();
      }
    }));
  });
});
