import { HttpClient} from '@angular/common/http';
import { Component, input, signal } from '@angular/core';
import { Injectable } from '@angular/core';
@Component({
  selector: 'app-primary-button',
  imports: [],
  template: `
    <button (click)="handleButtonClick()">
      {{label()}}
    </button>
    
  `,
  styles: ``
})

@Injectable({
  providedIn: 'root'
})




export class PrimaryButtonComponent {
  label = input('');
  constructor(private http: HttpClient) {}
  handleButtonClick(){
    console.log('Button Pressed');
    this.http.post('http://10.60.107.200:3000/button-pressed',{})
      .subscribe(response => {
        console.log('response',response);
      });
  }
}
