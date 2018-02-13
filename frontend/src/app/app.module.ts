import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { AppRoutingModule } from './/app-routing.module';
import { UsersComponent } from './users/users.component';
import { CommunitiesComponent } from './communities/communities.component';
import { UserService } from './user.service';
import { MessageService } from './message.service';

// import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

import { InfiniteScrollModule } from 'ngx-infinite-scroll';
import { MessagesComponent } from './messages/messages.component';
import { UserComponent } from './user/user.component';
import { GraphComponent } from './graph/graph.component';
import { GraphService } from './graph.service';
import { CommunityService } from './community.service';
import { ApiService } from './api.service';
import { SearchBoxComponent } from './search-box/search-box.component';
import { CommunityComponent } from './community/community.component';
import { NewYear2018GameComponent } from './new-year-2018-game/new-year-2018-game.component';
import { AboutComponent } from './about/about.component';
import { LoadingAnimationComponent } from './loading-animation/loading-animation.component';
import { LoadingAnimationService } from './loading-animation.service';
import { IndexComponent } from './index/index.component';


@NgModule({
    declarations: [
    AppComponent,
    SidebarComponent,
    UsersComponent,
    CommunitiesComponent,
    MessagesComponent,
    UserComponent,
    GraphComponent,
    SearchBoxComponent,
    CommunityComponent,
    NewYear2018GameComponent,
    AboutComponent,
    LoadingAnimationComponent,
    IndexComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        InfiniteScrollModule
    ],
    providers: [
        UserService,
        MessageService,
        GraphService,
        CommunityService,
        ApiService,
        LoadingAnimationService
    ],
    bootstrap: [ AppComponent ]
})
export class AppModule { }
