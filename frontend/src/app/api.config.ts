import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isDevMode } from '@angular/core';



export class ApiConfig {
	/*public static _API_URL = "/api";
	public static get API_URL(): string {
		if (isDevMode())
			return 'http://localhost:4444' + this._API_URL;

		return this._API_URL;
	};*/
	public static API_URL = "/api";
	public static USER_API_URL = `${ApiConfig.API_URL}/users`;
	public static USERS_API_URL = `${ApiConfig.API_URL}/users`;

	public static COMMUNITY_API_URL = `${ApiConfig.API_URL}/communities`;
	public static COMMUNITIES_API_URL = `${ApiConfig.API_URL}/communities`;

	public static GRAPH_URL = `${ApiConfig.API_URL}/graph`;

	public static NEW_YEAR_2018_GAME_URL = `${ApiConfig.API_URL}/new_year_2018_game`;
	public static NEW_YEAR_2018_GAME_SCOREBOARD_URL =
		`${ApiConfig.NEW_YEAR_2018_GAME_URL}/scoreboards`;
		public static NEW_YEAR_2018_GAME_TOP_URL =
		`${ApiConfig.NEW_YEAR_2018_GAME_URL}/top_items`;

	public static HTTP_OPTIONS = {
	    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
	};
}
