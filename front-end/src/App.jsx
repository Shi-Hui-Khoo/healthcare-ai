import Navbar from "./components/Navbar";
import AboutSection from "./components/AboutSection";
import MainPage from "./components/MainPage";
import "./styles/Navbar.css";
import "./styles/MainPage.css";
import "./styles/AboutSection.css";

function App() {
  return (
    <div>
      <Navbar />
      <MainPage />
      <AboutSection />
    </div>
  );
}

export default App;
