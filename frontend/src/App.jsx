import React, { useState } from 'react';
import axios from 'axios';
import { 
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  Download, Filter, BarChart3, PieChart as PieChartIcon,
  Loader2, AlertCircle, Info
} from 'lucide-react';
import { Button } from './components/ui/Button';
import { Input } from './components/ui/Input';
import { Label } from './components/ui/Label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/Card';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const COLORS = ['#10b981', '#ef4444', '#f59e0b', '#6b7280', '#8b5cf6'];

function App() {
  const [step, setStep] = useState('input');
  const [formData, setFormData] = useState({
    username: '',
    accessKey: '',
    testRunFilter: ''
  });
  const [reportData, setReportData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    project: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFilterChange = (e) => {
    const newFilters = {
      ...filters,
      [e.target.name]: e.target.value
    };
    setFilters(newFilters);
    applyFilters(newFilters);
  };

  const applyFilters = (currentFilters) => {
    let filtered = [...reportData];
    
    if (currentFilters.project) {
      filtered = filtered.filter(item => 
        item.project.toLowerCase().includes(currentFilters.project.toLowerCase())
      );
    }
    
    setFilteredData(filtered);
  };

  const generateReport = async () => {
    if (!formData.username || !formData.accessKey) {
      setError('Please provide both username and access key');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/generate-report`, formData);
      
      if (response.data.success) {
        setReportData(response.data.data);
        setFilteredData(response.data.data);
        setStep('report');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/download-report`, {
        reportData: filteredData
      }, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `browserstack_report_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download report');
    }
  };

  const getChartData = () => {
    const totals = filteredData.reduce((acc, item) => {
      acc.passed += item.passed;
      acc.failed += item.failed;
      acc.blocked += item.blocked;
      acc.untested += item.untested;
      acc.skipped += item.skipped;
      return acc;
    }, { passed: 0, failed: 0, blocked: 0, untested: 0, skipped: 0 });

    return [
      { name: 'Passed', value: totals.passed, color: '#10b981' },
      { name: 'Failed', value: totals.failed, color: '#ef4444' },
      { name: 'Blocked', value: totals.blocked, color: '#f59e0b' },
      { name: 'Untested', value: totals.untested, color: '#6b7280' },
      { name: 'Skipped', value: totals.skipped, color: '#8b5cf6' }
    ];
  };

  const getBarChartData = () => {
    return filteredData.map(item => ({
      name: item.testRun.length > 20 ? item.testRun.substring(0, 20) + '...' : item.testRun,
      Passed: item.passed,
      Failed: item.failed,
      Blocked: item.blocked
    }));
  };

  const getBarChartHeight = () => {
    const count = filteredData.length;
    const baseHeight = 50;
    const barHeight = 40;
    return Math.max(400, count * barHeight + baseHeight);
  };

  const resetForm = () => {
    setStep('input');
    setFormData({ username: '', accessKey: '', testRunFilter: '' });
    setReportData([]);
    setFilteredData([]);
    setFilters({ project: '' });
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-block">
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">
              BrowserStack Test Report Generator
            </h1>
            <div className="h-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full"></div>
          </div>
          <p className="text-gray-600 mt-4 text-lg">
            Generate comprehensive test reports with visual analytics
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg flex items-center gap-3 text-red-800 shadow-md animate-in fade-in slide-in-from-top-2 duration-300">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span className="font-medium">{error}</span>
          </div>
        )}

        {step === 'input' && (
          <Card className="max-w-2xl mx-auto shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl">Configuration</CardTitle>
              <CardDescription className="text-base">
                Enter your BrowserStack credentials and test run filter
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">BrowserStack Username</Label>
                <Input
                  id="username"
                  name="username"
                  placeholder="Enter your username"
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="accessKey">Access Key</Label>
                <Input
                  id="accessKey"
                  name="accessKey"
                  type="password"
                  placeholder="Enter your access key"
                  value={formData.accessKey}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="testRunFilter">
                  Test Run Name Filter (Optional)
                </Label>
                <Input
                  id="testRunFilter"
                  name="testRunFilter"
                  placeholder="e.g., regression cycle 1"
                  value={formData.testRunFilter}
                  onChange={handleInputChange}
                />
                <div className="flex items-start gap-2 p-3 bg-blue-50 rounded-md">
                  <Info className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-blue-800">
                    <strong>Filter Usage:</strong> Enter a keyword to filter test runs by name. 
                    Leave empty to fetch all test runs. The filter is case-insensitive and matches 
                    test runs containing the specified text.
                  </p>
                </div>
              </div>

              <Button 
                onClick={generateReport} 
                disabled={loading}
                className="w-full"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Report...
                  </>
                ) : (
                  'Generate Report'
                )}
              </Button>
            </CardContent>
          </Card>
        )}

        {step === 'report' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-6 p-6 bg-white rounded-xl shadow-md border border-gray-100">
              <div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">Test Report</h2>
                <p className="text-sm text-gray-500 mt-1">Showing {filteredData.length} test run{filteredData.length !== 1 ? 's' : ''}</p>
              </div>
              <div className="flex flex-wrap gap-2">
                <Button onClick={downloadReport} variant="outline" className="shadow-sm hover:shadow-md transition-shadow">
                  <Download className="mr-2 h-4 w-4" />
                  Download CSV
                </Button>
                <Button onClick={resetForm} variant="secondary" className="shadow-sm hover:shadow-md transition-shadow">
                  New Report
                </Button>
              </div>
            </div>

            <Card className="shadow-lg border-0 bg-gradient-to-br from-white to-gray-50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-xl">
                  <Filter className="w-5 h-5 text-blue-600" />
                  Filters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Label htmlFor="projectFilter">Project</Label>
                  <Input
                    id="projectFilter"
                    name="project"
                    placeholder="Filter by project"
                    value={filters.project}
                    onChange={handleFilterChange}
                  />
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="shadow-lg border-0 bg-gradient-to-br from-blue-50 to-blue-100 hover:shadow-xl transition-shadow">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-blue-700">
                    Total Test Runs
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-blue-900">{filteredData.length}</div>
                </CardContent>
              </Card>
              
              <Card className="shadow-lg border-0 bg-gradient-to-br from-indigo-50 to-indigo-100 hover:shadow-xl transition-shadow">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-indigo-700">
                    Total Tests
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-indigo-900">
                    {filteredData.reduce((sum, item) => sum + item.totalTests, 0)}
                  </div>
                </CardContent>
              </Card>
              
              <Card className="shadow-lg border-0 bg-gradient-to-br from-green-50 to-green-100 hover:shadow-xl transition-shadow">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-green-700">
                    Passed
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-green-700">
                    {filteredData.reduce((sum, item) => sum + item.passed, 0)}
                  </div>
                </CardContent>
              </Card>
              
              <Card className="shadow-lg border-0 bg-gradient-to-br from-red-50 to-red-100 hover:shadow-xl transition-shadow">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-red-700">
                    Failed
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-4xl font-bold text-red-700">
                    {filteredData.reduce((sum, item) => sum + item.failed, 0)}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="shadow-lg border-0 bg-white hover:shadow-xl transition-shadow">
                <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-t-lg">
                  <CardTitle className="flex items-center gap-2 text-xl">
                    <PieChartIcon className="w-5 h-5 text-blue-600" />
                    Test Status Distribution
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={350}>
                    <PieChart>
                      <Pie
                        data={getChartData()}
                        cx="50%"
                        cy="50%"
                        labelLine={true}
                        label={({ name, percent }) => percent > 0.02 ? `${name}: ${(percent * 100).toFixed(0)}%` : ''}
                        outerRadius={90}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {getChartData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="shadow-lg border-0 bg-white hover:shadow-xl transition-shadow">
                <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-t-lg">
                  <CardTitle className="flex items-center gap-2 text-xl">
                    <BarChart3 className="w-5 h-5 text-green-600" />
                    Test Results by Run
                  </CardTitle>
                  <CardDescription className="mt-2">
                    {filteredData.length > 10 ? 'Scroll to view all test runs' : `Showing all ${filteredData.length} test run${filteredData.length !== 1 ? 's' : ''}`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="overflow-x-auto">
                    <div style={{ minWidth: '600px', width: '100%', height: getBarChartHeight() }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={getBarChartData()} margin={{ top: 20, right: 30, left: 20, bottom: 100 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                          <XAxis 
                            dataKey="name" 
                            angle={-45} 
                            textAnchor="end" 
                            height={120}
                            interval={0}
                            tick={{ fontSize: 12 }}
                          />
                          <YAxis tick={{ fontSize: 12 }} />
                          <Tooltip 
                            contentStyle={{ 
                              backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                              border: '1px solid #e5e7eb',
                              borderRadius: '8px',
                              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                            }}
                          />
                          <Legend wrapperStyle={{ paddingTop: '20px' }} />
                          <Bar dataKey="Passed" fill="#10b981" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="Failed" fill="#ef4444" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="Blocked" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="shadow-lg border-0 bg-white">
              <CardHeader className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-t-lg">
                <CardTitle className="text-xl">Detailed Report</CardTitle>
                <CardDescription className="mt-2">Complete breakdown of all test runs</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto rounded-lg">
                  <table className="w-full text-sm">
                    <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
                      <tr>
                        <th className="px-4 py-4 text-left font-semibold text-gray-700 border-b-2 border-gray-200">Project</th>
                        <th className="px-4 py-4 text-left font-semibold text-gray-700 border-b-2 border-gray-200">Test Run</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Total</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Passed</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Failed</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Blocked</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Untested</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Skipped</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Execution %</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Pass %</th>
                        <th className="px-4 py-4 text-right font-semibold text-gray-700 border-b-2 border-gray-200">Fail %</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {filteredData.map((item, index) => {
                        const executionPercentage = item.totalTests > 0 
                          ? (((item.passed + item.failed + item.blocked) / item.totalTests) * 100).toFixed(2)
                          : 0;
                        
                        return (
                          <tr key={index} className="hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 transition-colors">
                            <td className="px-4 py-4 font-medium text-gray-900">{item.project}</td>
                            <td className="px-4 py-4 text-gray-700">{item.testRun}</td>
                            <td className="px-4 py-4 text-right font-semibold text-gray-900">{item.totalTests}</td>
                            <td className="px-4 py-4 text-right text-green-600 font-bold">{item.passed}</td>
                            <td className="px-4 py-4 text-right text-red-600 font-bold">{item.failed}</td>
                            <td className="px-4 py-4 text-right text-orange-600 font-bold">{item.blocked}</td>
                            <td className="px-4 py-4 text-right text-gray-600 font-medium">{item.untested}</td>
                            <td className="px-4 py-4 text-right text-purple-600 font-medium">{item.skipped}</td>
                            <td className="px-4 py-4 text-right">
                              <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                                executionPercentage >= 90 ? 'bg-green-100 text-green-700 border border-green-300' : 
                                executionPercentage >= 70 ? 'bg-blue-100 text-blue-700 border border-blue-300' : 
                                executionPercentage >= 50 ? 'bg-yellow-100 text-yellow-700 border border-yellow-300' : 'bg-red-100 text-red-700 border border-red-300'
                              }`}>
                                {executionPercentage}%
                              </span>
                            </td>
                            <td className="px-4 py-4 text-right">
                              <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                                item.passPercentage >= 80 ? 'bg-green-100 text-green-700 border border-green-300' : 
                                item.passPercentage >= 50 ? 'bg-yellow-100 text-yellow-700 border border-yellow-300' : 'bg-red-100 text-red-700 border border-red-300'
                              }`}>
                                {item.passPercentage}%
                              </span>
                            </td>
                            <td className="px-4 py-4 text-right">
                              <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                                item.failPercentage >= 20 ? 'bg-red-100 text-red-700 border border-red-300' : 
                                item.failPercentage >= 10 ? 'bg-yellow-100 text-yellow-700 border border-yellow-300' : 'bg-green-100 text-green-700 border border-green-300'
                              }`}>
                                {item.failPercentage}%
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
