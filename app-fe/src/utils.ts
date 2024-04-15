import numeral from "numeral";

export function fNum(target: any) {
    const formatted = numeral(+target).format('0.00a');
    const suffix = formatted.charAt(formatted.length - 1).toUpperCase();
    return formatted.slice(0, -1) + suffix;
}