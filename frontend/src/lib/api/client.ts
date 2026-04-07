import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 요청 인터셉터 - 토큰이 있으면 항상 첨부
// (공개 엔드포인트도 토큰이 있으면 그대로 사용; 백엔드가 무시하거나
//  인증된 사용자 정보를 활용)
apiClient.interceptors.request.use(
  (config) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 - 토큰 갱신 처리
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 401 에러 && 재시도하지 않은 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;

      // 리프레시 토큰이 있으면 토큰 갱신 시도
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          // 리프레시 실패 - 토큰 제거
          if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
          }
        }
      }

      // 리프레시 토큰이 없거나 갱신 실패한 경우
      // 공개 엔드포인트는 이미 요청 인터셉터에서 토큰 없이 요청되므로 여기 도달하지 않음
      // 인증 필요한 엔드포인트는 에러를 그대로 반환 (각 컴포넌트에서 처리)
    }

    return Promise.reject(error);
  }
);

export default apiClient;
