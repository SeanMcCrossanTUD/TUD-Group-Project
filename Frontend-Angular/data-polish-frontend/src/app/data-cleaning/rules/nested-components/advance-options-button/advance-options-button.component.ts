import { Component, OnDestroy } from '@angular/core';

import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-advance-options-button',
  templateUrl: './advance-options-button.component.html',
  styleUrls: ['./advance-options-button.component.css']
})
export class AdvanceOptionsButtonComponent {
  private params: any;

  agInit(params: any): void {
    this.params = params;
  }

  btnClickedHandler(event: any) {
    this.params.clicked(this.params.value);
  }

  refresh() {
    return false;
  }
}
