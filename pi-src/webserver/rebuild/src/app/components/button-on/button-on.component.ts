import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Component } from '@angular/core';

@Component({
  selector: 'app-button-on',
  imports: [],
  template: `
    <button (click)="handleButtonClick()">
      ON
    </button>
  `,
  styles: ``
})

@Injectable({
  providedIn: 'root'
})

export class ButtonONComponent {
  constructor(private http: HttpClient) {}
  handleButtonClick(){
    console.log('Button Pressed');
    this.http.post('http://192.168.12.1:3000/button-pressed-on',{})
      .subscribe(response => {
          console.log(response);
      });
  }
}
