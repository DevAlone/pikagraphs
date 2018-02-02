export class DateUtils {
	public static timestampToDateString(timestamp: number): string {
        var date = new Date(timestamp * 1000);
        var date_string = "";
        
        date_string += this.numberWithLeadingZeros(date.getFullYear(), 4);
        date_string += '.' + this.numberWithLeadingZeros(date.getMonth(), 2);
        date_string += '.' + this.numberWithLeadingZeros(date.getDate(), 2);
        date_string += ' ' + this.numberWithLeadingZeros(date.getHours(), 2);
        date_string += ':' + this.numberWithLeadingZeros(date.getMinutes(), 2);
        date_string += ':' + this.numberWithLeadingZeros(date.getSeconds(), 2);

        return date_string;
	}

	private static numberWithLeadingZeros(number: any, size: number) {
	    var result = number.toString();

	    while (result.length < size)
	    	result = "0" + result;

	    return result;
	}
}