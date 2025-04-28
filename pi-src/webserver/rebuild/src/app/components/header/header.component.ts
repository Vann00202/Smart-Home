import { Component,OnInit } from '@angular/core';
import { PrimaryButtonComponent } from "../primary-button/primary-button.component";
import { ButtonONComponent } from '../button-on/button-on.component';
import { ButtonOFFComponent } from '../button-off/button-off.component';
import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';


@Component({
  selector: 'app-header',
  imports: [PrimaryButtonComponent, ButtonOFFComponent, ButtonONComponent],
  template: `
  <div class="header">
  
    {{title}}
    <button (click)="handleButtonClick()">
      (Click for Status)
    </button>
    {{status}}

  </div>
  <div class="header">
    Light Switch: 
    <app-button-on></app-button-on>
    <app-button-off></app-button-off>
    <app-primary-button label = 'Toggle ON/OFF'/>
  </div>
  `,
  styles: `
  .header{
    background: rgba(0,0,0,.5);
    color: black;
    padding: 1rem;
  }
  `
})
@Injectable({
  providedIn: 'root'
})

export class HeaderComponent implements OnInit{
  title = 'Wired Living Lights Status: ';
  status = 'Undetermined';


  ngOnInit(){
    this.http.post('http://192.168.12.1:3000/button-status',{})
      .subscribe(response => {
        if(response == 0){
          this.status = 'ON';
        }else if(response == 1){
          this.status = 'OFF';
        }else{
          this.status = 'Undetermined';
        }
      });
  }
  constructor(private http: HttpClient) {}
  handleButtonClick(){
    window.location.reload();
    console.log('Button status Pressed');
    //192.168.12.1
    this.http.post('http://192.168.12.1:3000/button-status',{})
      .subscribe(response => {
        if(response == 0){
          this.status = 'ON';
        }else if(response == 1){
          this.status = 'OFF';
        }else{
          this.status = 'Undetermined';
        }
      });
  }
  
}
