import { InputComponent } from './../../basic-ui-elements/input/input.component';
import { ButtonComponent } from './../../basic-ui-elements/button/button.component';
import { CardConfiguration, CardComponent } from 'src/app/basic-ui-elements/card/card.component';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { LotHandlingComponent } from './lot-handling.component';
import { DebugElement, NgModule } from '@angular/core';
import { By } from '@angular/platform-browser';
import { SystemState } from 'src/app/system-status';
import { FormsModule } from '@angular/forms';

describe('LotHandlingComponent', () => {
  let component: LotHandlingComponent;
  let fixture: ComponentFixture<LotHandlingComponent>;
  let debugElement: DebugElement;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LotHandlingComponent, ButtonComponent, InputComponent, CardComponent],
      imports: [FormsModule],
      schemas: []
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

  it('load lot button should be disabled in states connecting, testing, ready and unloading but enabled in state initialized', () => {

    // connecting
    (component as any).handleServerMessage({payload: {state: SystemState.connecting}});
    fixture.detectChanges();

    let buttons = fixture.debugElement.queryAll(By.css('app-button'));
    let loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');
    expect(loadLotButton.hasAttribute('disabled')).toBeTruthy();


    // testing
    (component as any).handleServerMessage({payload: {state: SystemState.testing}});
    fixture.detectChanges();

    buttons = fixture.debugElement.queryAll(By.css('app-button'));
    loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');
    expect(loadLotButton.hasAttribute('disabled')).toBeTruthy();

    // unloading
    (component as any).handleServerMessage({payload: {state: SystemState.unloading}});
    fixture.detectChanges();

    buttons = fixture.debugElement.queryAll(By.css('app-button'));
    loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');
    expect(loadLotButton.hasAttribute('disabled')).toBeTruthy();

    // ready
    (component as any).handleServerMessage({payload: {state: SystemState.ready}});
    fixture.detectChanges();

    buttons = fixture.debugElement.queryAll(By.css('app-button'));
    loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');
    expect(loadLotButton.hasAttribute('disabled')).toBeTruthy();

    // initialized
    (component as any).handleServerMessage({payload: {state: SystemState.initialized}});
    fixture.detectChanges();

    buttons = fixture.debugElement.queryAll(By.css('app-button'));
    loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');
    expect(loadLotButton.hasAttribute('disabled')).toBeFalsy();
  });

  it('should call method sendLotNumber when button clicked', async(() => {

    // initialized
    (component as any).handleServerMessage({payload: {state: SystemState.initialized}});
    fixture.detectChanges();

    let spy = spyOn(component, 'sendLotNumber');

    let buttons = fixture.debugElement.queryAll(By.css('app-button'));
    let loadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Load Lot')[0].nativeElement.querySelector('button');

    loadLotButton.click();
    fixture.detectChanges();

    expect(spy).toHaveBeenCalled();
  }));

  describe('When system state is "ready"', () => {
    it('unload lot button should be active', async(() => {

      // ready
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();

      let buttons = fixture.debugElement.queryAll(By.css('app-button'));
      let unloadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Unload Lot')[0].nativeElement.querySelector('button');

      expect(unloadLotButton.hasAttribute('disabled')).toBeFalsy('unload lot button is expected to be active');
    }));

    it('should call method unloadLotButtonClicked when button clicked', async(() => {

      // ready
      (component as any).handleServerMessage({payload: {state: SystemState.ready}});
      fixture.detectChanges();
      let spy = spyOn(component, 'unloadLot');

      let buttons = fixture.debugElement.queryAll(By.css('app-button'));
      let unloadLotButton = buttons.filter(e => e.nativeElement.innerText === 'Unload Lot')[0].nativeElement.querySelector('button');
      unloadLotButton.click();
      fixture.detectChanges();

      expect(spy).toHaveBeenCalled();
    }));
  });
});
