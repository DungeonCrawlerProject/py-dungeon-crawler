/*
 * The Manager that oversees all Steam functionality
 * Uses SteamAPI Version: 1.0.13
 * By: Sean McClanahan
 * Last Modified: 08/18/2023
 * Documentation: https://steamworks.github.io/installation/
 */


#if !(UNITY_STANDALONE_WIN || UNITY_STANDALONE_LINUX || UNITY_STANDALONE_OSX || STEAMWORKS_WIN || STEAMWORKS_LIN_OSX)
#define DISABLESTEAMWORKS
#endif

using UnityEngine;
#if !DISABLESTEAMWORKS
using System.Collections;
using Steamworks;
#endif


[DisallowMultipleComponent]
public class SteamManager : MonoBehaviour {
	
	// the #if statement allows the compilier to do less work depending on how this file is being started.
	#if !DISABLESTEAMWORKS
		protected static bool s_EverInitialized = false;
		// This is the Game ID, 480 refers to SpaceWars which is specifically used for development purposes.
		public static AppId_t MYAPPID = (AppId_t)480;
		protected static SteamManager s_instance;
		protected static SteamManager Instance {
			get {
				if (s_instance == null) {
					return new GameObject("SteamManager").AddComponent<SteamManager>();
				}
				else {
					return s_instance;
				}
			}
		}

		protected bool m_bInitialized = false;
		public static bool Initialized {
			get {
				return Instance.m_bInitialized;
			}
		}

		protected SteamAPIWarningMessageHook_t m_SteamAPIWarningMessageHook;

		[AOT.MonoPInvokeCallback(typeof(SteamAPIWarningMessageHook_t))]
		protected static void SteamAPIDebugTextHook(int nSeverity, System.Text.StringBuilder pchDebugText) {
			Debug.LogWarning(pchDebugText);
		}

	#if UNITY_2019_3_OR_NEWER
		// In case of disabled Domain Reload, reset static members before entering Play Mode.
		[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
		private static void InitOnPlayMode()
		{
			s_EverInitialized = false;
			s_instance = null;
		}
	#endif

		protected virtual void Awake() {
			// Only one instance of SteamManager at a time!
			if (s_instance != null) {
				Destroy(gameObject);
				return;
			}
			s_instance = this;
			
			// This is almost always an error.
			if(s_EverInitialized) {
				// Limit Steamworks functions in OnDestroy, use OnDisable when possible.
				throw new System.Exception("Tried to Initialize the SteamAPI twice in one session!");
			}

			// SteamManager Instance to persist across scenes.
			DontDestroyOnLoad(gameObject);

			if (!Packsize.Test()) {
				Debug.LogError("[Steamworks.NET] Packsize Test returned false, the wrong version of Steamworks.NET is being run in this platform.", this);
			}

			if (!DllCheck.Test()) {
				Debug.LogError("[Steamworks.NET] DllCheck Test returned false, One or more of the Steamworks binaries seems to be the wrong version.", this);
			}
			
			// If Steam is not running properly SteamAPI_RestartAppIfNecessary starts the Steam client and reboots game.
			try {
				// Steam AppID assigned by Valve, should replace AppId_t.Invalid with it and remove steam_appid.txt
				if (SteamAPI.RestartAppIfNecessary(MYAPPID)) {
					Debug.Log("[Steamworks.NET] is restarting the program due to NRM.");
					Application.Quit();
					return;
				}
			} catch (System.DllNotFoundException e) {
				Debug.LogError("[Steamworks.NET] Could not load [lib]steam_api.dll/so/dylib. It's likely not in the correct location. Refer to the README for more details.\n" + e, this);

				Application.Quit();
				return;
			}

			// Initializing the Steamworks API.
			// Valve's documentation: https://partner.steamgames.com/doc/sdk/api#initialization_and_shutdown
			m_bInitialized = SteamAPI.Init();
			if (!m_bInitialized) {
				Debug.LogError("[Steamworks.NET] SteamAPI_Init() failed. Refer to Valve's documentation or the comment above this line for more information.", this);

				return;
			}

			s_EverInitialized = true;
		}

		// This should only ever get called on first load and after an Assembly reload, You should never Disable the Steamworks Manager yourself.
		protected virtual void OnEnable() {
			if (s_instance == null) {
				s_instance = this;
			}

			if (!m_bInitialized) {
				return;
			}

			if (m_SteamAPIWarningMessageHook == null) {
				// Set up our callback to receive warning messages from Steam.
				// You must launch with "-debug_steamapi" in the launch args to receive warnings.
				m_SteamAPIWarningMessageHook = new SteamAPIWarningMessageHook_t(SteamAPIDebugTextHook);
				SteamClient.SetWarningMessageHook(m_SteamAPIWarningMessageHook);
			}
		}

		// OnApplicationQuit gets called too early to shutdown the SteamAPI.
		// Because the SteamManager should be persistent and never disabled or destroyed we can shutdown the SteamAPI here.
		// Don't perform any Steamworks work in other OnDestroy functions as the order may freeze during Shutdown. Prefer OnDisable().
		protected virtual void OnDestroy() {
			if (s_instance != this) {
				return;
			}

			s_instance = null;

			if (!m_bInitialized) {
				return;
			}

			SteamAPI.Shutdown();
		}

		protected virtual void Update() {
			if (!m_bInitialized) {
				return;
			}

			// Run Steam client callbacks
			SteamAPI.RunCallbacks();
		}
	#else
		public static bool Initialized {
			get {
				return false;
			}
		}
	#endif // !DISABLESTEAMWORKS
}
