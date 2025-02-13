import myImage from '../images/hospital.png';

const MainPage = () => {
  return (
    <section className="main-page">
      <div className="main-content">
        <h2 className="sub-title">Committed to Wellness</h2>
        <h1 className="main-title">
          We Care About Your <span className="highlight">Health</span>
        </h1>
        <p className="description">
          Advancing healthcare with cutting-edge technology and compassionate care.<br></br>
          Ready 24/7 to provide life-saving care when every second counts.
        </p>
        <button className="appointment-btn">Read More →</button>
      </div>
      <img src={myImage} alt="My Image" className="main-image" />
    </section>
  );
};



  window.watsonAssistantChatOptions = {
    integrationID: "01fb7989-3535-4a77-a4e6-de11d8f0fbef", // The ID of this integration.
    region: "us-south", // The region your integration is hosted in.
    serviceInstanceID: "8a018efa-7da0-4235-babc-b39b6ffd265b", // The ID of your service instance.
    onLoad: async (instance) => { await instance.render(); }
  };
  setTimeout(function(){
    const t=document.createElement('script');
    t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
    document.head.appendChild(t);
  });



export default MainPage;
