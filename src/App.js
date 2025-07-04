import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import LandingPage from './components/website/LandingPage.jsx';
import SiteMap from './components/website/landingPageComponents/siteMap.tsx';
import CriteriaPage from './components/website/enrollmentProcess.tsx';
import ProgramsPage from './components/website/programsPage.tsx';
import BasicProfileForm from './components/website/basicProfileForm.tsx';
import FAQPage from './components/website/faqPage.tsx';
import ContactPage from './components/website/contactPage.tsx';
import ProgramTimeline from './components/website/programSchedule.tsx';
import IndividualProgramDetail from './components/website/indivisualProgram.tsx';
import TrainerMainPage from './components/trainerMainPage.tsx';
import { Login } from './components/login.tsx';
import QuizzesPage from './components/trainer_portal/quizzesPage.tsx';
import AssignmentsPage from './components/trainer_portal/assignmentsPage.tsx';
import ContentPage from './components/trainer_portal/contentPage.tsx';
import VirtualSessionPage from './components/trainer_portal/virtualSessionPage.tsx';
import ViewProfile from './components/trainer_portal/viewProfile.tsx';
import EditProfile from './components/trainer_portal/editProfile.tsx';
const ProtectedRoute = ({ children }) => {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('access_token');
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  return isAuthenticated ? children : null;
};

function App() {
  useEffect(() => {
    // Add a response interceptor
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          // If we receive a 401 error, redirect to login
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );

    // Clean up the interceptor when the component unmounts
    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/sitemap" element={<SiteMap />} />
        <Route path="/criteria" element={<CriteriaPage />} />
        <Route path="/programs" element={<ProgramsPage />} />
        <Route path="/apply" element={<BasicProfileForm />} />
        <Route path="/faq" element={<FAQPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/trainingSchedule" element={<ProgramTimeline />} />
        <Route path="/program/:programId" element={<IndividualProgramDetail />} />
        <Route path="/login" element={<Login />} />
        <Route 
          path="/trainer" 
          element={
            <ProtectedRoute>
              <TrainerMainPage />
            </ProtectedRoute>
          } 
        />
        <Route path="/quizzes" element={<QuizzesPage />} />
        <Route path="/assignments" element={<AssignmentsPage />} />
        <Route path="/content" element={<ContentPage />} />
        <Route path="/virtual-sessions" element={<VirtualSessionPage />} />
        <Route path="/profile" element={<ViewProfile />} />
        <Route path="/profile/edit" element={<EditProfile />} />
      </Routes>
    </Router>
  );
}

export default App;

