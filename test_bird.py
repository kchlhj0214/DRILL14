"""창 없이 실행: python -m unittest test_bird.py"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


class BirdFlightTests(unittest.TestCase):
    def setUp(self):
        self.image = Mock(w=918, h=506)
        self.framework = types.SimpleNamespace(frame_time=0.0)
        pico = types.SimpleNamespace(
            get_canvas_width=lambda: 1600,
            load_image=Mock(return_value=self.image),
        )
        spec = importlib.util.spec_from_file_location(
            'bird_under_test', Path(__file__).with_name('bird.py'))
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, pico2d=pico, game_framework=self.framework):
            spec.loader.exec_module(self.module)

    def simulate(self, fps, seconds):
        bird = self.module.Bird(400, 300)
        self.framework.frame_time = 1 / fps
        for _ in range(fps * seconds):
            bird.update()
        return bird

    def test_equal_elapsed_time_at_different_frame_rates(self):
        birds = [self.simulate(fps, 12) for fps in (30, 60, 144)]
        for bird in birds[1:]:
            self.assertAlmostEqual(bird.x, birds[0].x)
            # 순환 위상에서 14 직전과 0 직후는 같은 경계이다.
            phase_error = (bird.frame - birds[0].frame + 7) % 14 - 7
            self.assertAlmostEqual(phase_error, 0)
            self.assertEqual(bird.dir, birds[0].dir)

    def test_large_time_step_preserves_multiple_reflections(self):
        expected = self.simulate(60, 120)
        bird = self.module.Bird(400, 300)
        self.framework.frame_time = 120
        bird.update()
        self.assertAlmostEqual(bird.x, expected.x)
        self.assertEqual(bird.dir, expected.dir)
        self.assertTrue(40 <= bird.x <= 1560)

    def test_exact_edges_face_inwards(self):
        for x, direction in ((40, 1), (1560, -1)):
            bird = self.module.Bird(x, 300, -direction)
            bird.update()
            self.assertEqual(bird.x, x)
            self.assertEqual(bird.dir, direction)

    def test_all_frames_are_valid_and_left_flight_is_flipped(self):
        bird = self.module.Bird(400, 300, -1)
        for frame in range(14):
            bird.frame = frame
            bird.draw()
            x, y, w, h, angle, flip, *_ = self.image.clip_composite_draw.call_args.args
            self.assertTrue(0 <= x < x + w <= 918)
            self.assertTrue(0 <= y < y + h <= 506)
            self.assertEqual(flip, 'h')
        self.assertEqual((x, y), (550, 0))
        bird.frame = 13
        self.framework.frame_time = 1 / self.module.FLIGHT_FRAMES_PER_SECOND
        bird.update()
        self.assertAlmostEqual(bird.frame, 0)

    def test_image_is_shared(self):
        birds = [self.module.Bird(100, 300) for _ in range(10)]
        self.assertTrue(all(b.image is self.image for b in birds))
        self.module.load_image.assert_called_once_with('bird_animation.png')


if __name__ == '__main__':
    unittest.main()
