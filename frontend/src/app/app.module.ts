import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { AppRoutingModule } from './/app-routing.module';
import { UsersComponent } from './users/users.component';
import { CommunitiesComponent } from './communities/communities.component';
import { UserService } from './user.service';
// import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';


@NgModule({
    declarations: [
    AppComponent,
    SidebarComponent,
    UsersComponent,
    CommunitiesComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule
    ],
    providers: [
        UserService
        // HttpClient
    ],
    bootstrap: [ AppComponent ]
})
export class AppModule { }
