import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-article',
  templateUrl: './article.component.html',
  styleUrls: ['./article.component.css']
})
export class ArticleComponent implements OnInit {

  @Input() article : any;
  constructor() { }

  ngOnInit(): void {
  }

  nafigate(id:number){
    if(id == 0){
      alert("prev");
    }
    if(id == 1){
      alert("next");
    }
  }
}
