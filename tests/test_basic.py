def test_health_check():
    """Test basic health check functionality"""
    try:
        from src.monitor import PipelineMonitor
        
        monitor = PipelineMonitor()
        result = monitor.check_pipeline_health()
        
        assert hasattr(result, 'status'), "Health check should have status"
        assert hasattr(result, 'timestamp'), "Health check should have timestamp"
        assert hasattr(result, 'components'), "Health check should have components"
        return True
    except Exception as e:
        raise AssertionError(f"Health check test failed: {e}")

def test_status_report():
    """Test status report generation"""
    try:
        from src.monitor import PipelineMonitor
        
        monitor = PipelineMonitor()
        report = monitor.get_status_report()
        
        assert 'current_status' in report, "Report should have current_status"
        assert 'suggested_action' in report, "Report should have suggested_action"
        assert 'components_checked' in report or 'health_check_results' in report, "Report should have component info"
        return True
    except Exception as e:
        raise AssertionError(f"Status report test failed: {e}")

if __name__ == "__main__":
    test_health_check()
    test_status_report()
    print("✅ All basic tests passed!")