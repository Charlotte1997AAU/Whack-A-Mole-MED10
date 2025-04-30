using UnityEngine;

public class StateManager : MonoBehaviour
{
    private GameObject WebSocket;
    private GameObject unityLogger;
    private GameObject myoLogger;
    private GameObject wall;
    private MyoLogger logger;
    private LoggingManager loggingManager;
    private Hover hover;
    private testLogger testLogger;

    public enum State { Training, Testing }
    [SerializeField] public State state;

    void Start()
    {
        WebSocket = GameObject.Find("websocket Manager");
        unityLogger = GameObject.Find("Unity Logger");
        myoLogger = GameObject.Find("Myo Logger");
        wall = GameObject.Find("Wall");
        loggingManager = myoLogger.GetComponent<LoggingManager>();
        hover = wall.GetComponent<Hover>();
        testLogger = WebSocket.GetComponent<testLogger>();
    }

    // Update is called once per frame
    void Update()
    {
        if(state == State.Testing)
        {
            WebSocket.SetActive(true);
            unityLogger.SetActive(false);
            logger = myoLogger.GetComponent<MyoLogger>();
            logger.logData = false;
            loggingManager.enabled = false;
            hover.enabled = false;
            testLogger.testing = true;
        }
        if(state == State.Training)
        {
            WebSocket.SetActive(false);
            unityLogger.SetActive(true);
            loggingManager.enabled = true;
        }
    }
}
