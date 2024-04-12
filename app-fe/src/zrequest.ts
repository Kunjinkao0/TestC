import axios, { AxiosResponse } from 'axios';

export interface ApiResponse<T = any> {
    code: number;
    data: T;
    msg: string;
}

axios.interceptors.response.use(
    (response: AxiosResponse<ApiResponse>) => {
        const { status: resultStatus, data: resultData } = response;
        if (resultStatus === 200) {
            if (resultData.code === 1) {
                return resultData.data;
            } else {
                return resultData;
            }
        } else {
            return response;
        }
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axios;