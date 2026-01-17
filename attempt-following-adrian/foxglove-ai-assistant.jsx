import React, { useState, useRef } from 'react';
import { Loader2, Sparkles, Clock, Zap, AlertCircle, Copy, Check } from 'lucide-react';

const FoxgloveAIAssistant = () => {
  const [datasetInput, setDatasetInput] = useState('');
  const [topicListInput, setTopicListInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const jsonRef = useRef(null);

  const exampleInputs = [
    "KITTI-360 downloaded example",
    "ROS bag with LiDAR and camera",
    "Autonomous vehicle data: cameras, LiDAR, IMU"
  ];

  const exampleTopics = `/camera/image_raw
/velodyne_points
/tf`;

  const analyzeDataset = () => {
    if (!datasetInput.trim()) {
      setError('Please describe your dataset first');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    setTimeout(() => {
      setResult(generateResult(datasetInput, topicListInput));
      setLoading(false);
    }, 800);
  };

  const parseTopicList = (topicText) => {
    if (!topicText.trim()) return null;
    
    const lines = topicText.split(/[,\n]/).map(l => l.trim()).filter(l => l && l.startsWith('/'));
    const topics = [];
    
    for (const line of lines) {
      const name = line.split(/\s+/)[0]; // Get just the topic name
      let type = "unknown";
      
      if (name.includes('image') || name.includes('camera')) type = "sensor_msgs/Image";
      else if (name.includes('point') || name.includes('velodyne')) type = "sensor_msgs/PointCloud2";
      else if (name.includes('scan')) type = "sensor_msgs/LaserScan";
      else if (name.includes('imu')) type = "sensor_msgs/Imu";
      else if (name.includes('odom')) type = "nav_msgs/Odometry";
      else if (name.includes('tf')) type = "tf2_msgs/TFMessage";
      else if (name.includes('gps') || name.includes('nav')) type = "sensor_msgs/NavSatFix";
      
      topics.push({ name, type, priority: "high", description: "User-provided topic" });
    }
    
    return topics.length > 0 ? topics : null;
  };

  const generateResult = (description, topicText) => {
    const lower = description.toLowerCase();
    const isKitti360Example = lower.includes('kitti-360 downloaded example');
    const hasLidar = lower.includes('lidar') || lower.includes('velodyne') || lower.includes('point');
    const hasCamera = lower.includes('camera') || lower.includes('stereo') || lower.includes('image');
    
    // Check if user provided actual topics
    const parsedTopics = parseTopicList(topicText);
    
    let topics;
    let datasetType;
    
    if (parsedTopics) {
      // Use exact topic names from user input
      datasetType = "Custom Dataset (topics provided)";
      topics = parsedTopics;
    } else if (isKitti360Example) {
      // Only use KITTI-360 specific names if explicitly requested
      datasetType = "KITTI-360 Downloaded Example";
      topics = [
        { name: "/camera_00_semantic/image", type: "sensor_msgs/Image", description: "KITTI-360 semantic camera", priority: "high" },
        { name: "/velodyne_pointcloud", type: "sensor_msgs/PointCloud2", description: "KITTI-360 Velodyne LiDAR", priority: "high" },
        { name: "/tf", type: "tf2_msgs/TFMessage", description: "Transform tree", priority: "high" }
      ];
    } else {
      // Default to standard ROS names
      datasetType = lower.includes('kitti') ? "KITTI Dataset (standard ROS names)" : "ROS Dataset";
      topics = [
        ...(hasCamera ? [{ name: "/camera/image_raw", type: "sensor_msgs/Image", description: "Camera feed", priority: "high" }] : []),
        ...(hasLidar ? [{ name: "/velodyne_points", type: "sensor_msgs/PointCloud2", description: "LiDAR point cloud", priority: "high" }] : []),
        { name: "/tf", type: "tf2_msgs/TFMessage", description: "Transform tree", priority: "high" }
      ];
    }

    // Find primary topics for layout
    const pointCloudTopic = topics.find(t => t.type.includes('PointCloud'));
    const imageTopic = topics.find(t => t.type.includes('Image'));

    return {
      datasetType,
      topics,
      frameSettings: {
        fixedFrame: "map",
        fixedFrameReason: "World-fixed reference frame",
        displayFrame: pointCloudTopic ? "velodyne" : "base_link",
        displayFrameReason: "Sensor-centric view"
      },
      pointCloudSettings: {
        pointSize: 4, colorMode: "colormap", colorField: "z", valueMin: 0, valueMax: 30,
        reasoning: "Height-based coloring for obstacle visibility."
      },
      layoutSummary: parsedTopics 
        ? `Using ${topics.length} user-provided topics` 
        : "Default ROS topic names - paste your actual topic list for exact match",
      detectedLidarTopic: pointCloudTopic?.name || "/velodyne_points",
      detectedImageTopic: imageTopic?.name || "/camera/image_raw"
    };
  };

  const generateFoxgloveLayout = () => {
    if (!result) return '';

    const layout = {
      configById: {
        "3D!1": {
          cameraState: {
            perspective: true,
            distance: 75,
            phi: 80,
            thetaOffset: 0,
            targetOffset: [0, 0, 0]
          },
          followMode: "follow-pose",
          topics: {
            [result.detectedLidarTopic]: {
              visible: true,
              pointSize: 4
            }
          },
          layers: {
            grid: {
              visible: true
            }
          }
        },
        "Image!1": {
          imageTopic: result.detectedImageTopic
        }
      },
      globalVariables: {},
      userNodes: {},
      playbackConfig: {
        speed: 1
      },
      layout: {
        direction: "row",
        first: "3D!1",
        second: "Image!1",
        splitPercentage: 60
      }
    };

    return JSON.stringify(layout, null, 2);
  };

  const selectJson = () => {
    if (jsonRef.current) {
      jsonRef.current.select();
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Sparkles className="w-6 h-6 text-blue-600" />
            <h1 className="text-2xl font-bold text-slate-900">Foxglove AI Assistant</h1>
          </div>
          <p className="text-slate-600">Configure visualization in minutes, not hours</p>
        </div>

        <div className="grid md:grid-cols-2 gap-3 mb-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Clock className="w-5 h-5 text-red-600" />
              <h3 className="font-semibold text-red-900">Before: Manual</h3>
            </div>
            <p className="text-red-800 text-sm">4+ hours, wrong topics, frame confusion</p>
          </div>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-1">
              <Zap className="w-5 h-5 text-green-600" />
              <h3 className="font-semibold text-green-900">After: AI-Guided</h3>
            </div>
            <p className="text-green-800 text-sm">5 minutes, exact topics, ready to import</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 mb-4">
          <h2 className="text-lg font-semibold text-slate-900 mb-3">Describe Your Dataset</h2>
          
          <textarea
            className="w-full h-20 p-3 border-2 border-slate-300 rounded-lg focus:border-blue-500 focus:outline-none font-mono text-sm"
            placeholder="Example: ROS bag with LiDAR and camera"
            value={datasetInput}
            onChange={(e) => setDatasetInput(e.target.value)}
          />

          <div className="flex flex-wrap gap-2 mt-2 mb-4">
            {exampleInputs.map((example, i) => (
              <button key={i} className="text-xs px-2 py-1 bg-slate-100 hover:bg-slate-200 rounded-full text-slate-700"
                onClick={() => setDatasetInput(example)}>
                {example}
              </button>
            ))}
          </div>

          <h2 className="text-lg font-semibold text-slate-900 mb-2">Paste Your Topic List <span className="text-sm font-normal text-slate-500">(optional but recommended)</span></h2>
          <p className="text-xs text-slate-500 mb-2">Run <code className="bg-slate-100 px-1 rounded">mcap info your-file.mcap</code> or paste from Foxglove Topics panel</p>
          
          <textarea
            className="w-full h-24 p-3 border-2 border-slate-300 rounded-lg focus:border-blue-500 focus:outline-none font-mono text-sm"
            placeholder={`/camera/image_raw\n/velodyne_points\n/tf`}
            value={topicListInput}
            onChange={(e) => setTopicListInput(e.target.value)}
          />
          
          <button 
            className="text-xs text-blue-600 hover:text-blue-800 mt-1 mb-3"
            onClick={() => setTopicListInput(exampleTopics)}
          >
            Load example topics
          </button>

          {error && (
            <div className="mb-3 p-2 bg-yellow-50 border border-yellow-200 rounded flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-yellow-600" />
              <span className="text-sm text-yellow-800">{error}</span>
            </div>
          )}

          <button onClick={analyzeDataset} disabled={loading || !datasetInput.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2">
            {loading ? <><Loader2 className="w-4 h-4 animate-spin" />Analyzing...</> : <><Sparkles className="w-4 h-4" />Generate Configuration</>}
          </button>
        </div>

        {result && (
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
            <h2 className="text-xl font-bold text-slate-900 border-b pb-2">🎯 {result.datasetType}</h2>
            <p className="text-slate-600 text-sm">{result.layoutSummary}</p>

            <div>
              <h3 className="font-semibold text-slate-900 mb-2">📡 Topics</h3>
              <div className="space-y-1">
                {result.topics.map((topic, i) => (
                  <div key={i} className="flex items-center gap-2 p-2 bg-slate-50 rounded text-sm">
                    <span className={`px-1.5 py-0.5 rounded text-xs font-semibold ${topic.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>{topic.priority}</span>
                    <code className="text-blue-600">{topic.name}</code>
                    <span className="text-slate-400 text-xs">({topic.type})</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 bg-purple-50 rounded-lg">
                <div className="text-xs text-purple-700 font-semibold">Fixed Frame</div>
                <code className="text-purple-900">{result.frameSettings.fixedFrame}</code>
              </div>
              <div className="p-3 bg-indigo-50 rounded-lg">
                <div className="text-xs text-indigo-700 font-semibold">Display Frame</div>
                <code className="text-indigo-900">{result.frameSettings.displayFrame}</code>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-slate-900">📦 Layout JSON (select all & copy)</h3>
                <button onClick={selectJson} className="flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded">
                  {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                  {copied ? 'Selected!' : 'Select All'}
                </button>
              </div>
              <textarea
                ref={jsonRef}
                readOnly
                value={generateFoxgloveLayout()}
                className="w-full h-48 p-3 bg-slate-900 text-green-400 rounded-lg text-xs font-mono resize-none"
              />
              <p className="text-xs text-slate-500 mt-2">
                In Foxglove: File → Import Layout → paste JSON
              </p>
            </div>
          </div>
        )}

        <div className="text-center mt-6 text-xs text-slate-400">
          <p>💡 Pro tip: Paste actual topics for exact match. The future: auto-detect from MCAP files.</p>
        </div>
      </div>
    </div>
  );
};

export default FoxgloveAIAssistant;