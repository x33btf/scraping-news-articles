import { Component, OnInit } from '@angular/core';
import { SharedService } from './shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'AngularApp';
  NewsList:any=[];
  site :string[] = [];
  selectedSite : string = "";
  clickedArticle : any;

  constructor( private service:SharedService) {}

  ngOnInit(): void{
    this.refreshNewsList();
    
  }

  refreshNewsList(){
    
    this.service.getNewsList().subscribe(data=>{
      
      this.NewsList=data;
      this.getAllsite();
      
    });
  }
  getAllsite(){
    this.NewsList.forEach((element:any) => {
      
      if(this.site.includes(element.site) == false){
        this.site.push(element.site);
      }
    });
    this.selectedSite=this.site[0];
    this.clickedArticle = this.NewsList[0];
  }
  changeSite(item:any){
    this.selectedSite = item;
  }
  showarticle(item:any){
    this.clickedArticle = item;
  }
}

