import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';
import UserNavbar from './UserNavbar';

const Documentation = () => {
  const jwtToken = localStorage.getItem('accessToken');
  console.log('jwtToken:', jwtToken);

  return (
    <div className="min-h-screen">
      <UserNavbar/>
      <div className="container mx-auto mt-8">
      <SwaggerUI
          url="http://localhost:8000/openapi.json"
          requestInterceptor={(request) => {
            // Set the Authorization header with the JWT token
            request.headers['Authorization'] = `Bearer ${jwtToken}`;
            return request;
          }}
        />
      </div>
    </div>
  );
};

export default Documentation;
