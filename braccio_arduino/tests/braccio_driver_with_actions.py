#! /usr/bin/env python

import rospy

import actionlib

import actionlib_tutorials.msg
from control_msgs.msg import FollowJointTrajectoryAction
from std_msgs.msg import Float32
from threading import Thread

class Segment():
    def __init__(self, num_joints):
        self.start_time = 0.0  # trajectory segment start time
        self.duration = 0.0  # trajectory segment duration
        self.positions = [0.0] * num_joints
        self.velocities = [0.0] * num_joints


class JointTrajectoryActionController():
    def __init__(self, controller_namespace, controllers):
        print "I'm inside the __init__(arg1,arg2,arg3)"
        self.update_rate = 1000
        self.state_update_rate = 50
        self.trajectory = []

        self.controller_namespace = controller_namespace
        self.joint_names = [c for c in controllers]

        self.joint_to_controller = {}
        for c in controllers:
            self.joint_to_controller[c.joint_name] = c

        # self.port_to_joints = {}
        # for c in controllers:
        #     if c.port_namespace not in self.port_to_joints: self.port_to_joints[c.port_namespace] = []
        #     self.port_to_joints[c.port_namespace].append(c.joint_name)
        #
        # self.port_to_io = {}
        # for c in controllers:
        #     if c.port_namespace in self.port_to_io: continue
        #     self.port_to_io[c.port_namespace] = c.dxl_io

        self.joint_states = dict(zip(self.joint_names, [c.joint_state for c in controllers]))
        self.num_joints = len(self.joint_names)
        self.joint_to_idx = dict(zip(self.joint_names, range(self.num_joints)))


    # def __init__(self,name):
    #     print "I'm inside the __init__(arg1,arg2)"
    #     ns = self.controller_namespace + '/joint_trajectory_action_node/constraints'
    #     self.goal_time_constraint = rospy.get_param(ns + '/goal_time', 0.0)
    #     self.stopped_velocity_tolerance = rospy.get_param(ns + '/stopped_velocity_tolerance', 0.01)
    #     self.goal_constraints = []
    #     self.trajectory_constraints = []
    #     self.min_velocity = rospy.get_param(self.controller_namespace + '/joint_trajectory_action_node/min_velocity', 0.1)
    #
    #     for joint in self.joint_names:
    #         self.goal_constraints.append(rospy.get_param(ns + '/' + joint + '/goal', -1.0))
    #         self.trajectory_constraints.append(rospy.get_param(ns + '/' + joint + '/trajectory', -1.0))
    #
    #     # Message containing current state for all controlled joints
    #     self.msg = FollowJointTrajectoryFeedback()
    #     self.msg.joint_names = self.joint_names
    #     self.msg.desired.positions = [0.0] * self.num_joints
    #     self.msg.desired.velocities = [0.0] * self.num_joints
    #     self.msg.desired.accelerations = [0.0] * self.num_joints
    #     self.msg.actual.positions = [0.0] * self.num_joints
    #     self.msg.actual.velocities = [0.0] * self.num_joints
    #     self.msg.error.positions = [0.0] * self.num_joints
    #     self.msg.error.velocities = [0.0] * self.num_joints
    #
    #     return True

#########################################################

    # def __init__(self, name):
    #     self._action_name = name+"/follow_joint_trajectory"
    #     self.action_server = actionlib.SimpleActionServer(self._action_name, FollowJointTrajectoryAction, execute_cb=self.process_follow_trajectory, auto_start = False)
    #     print "lorenzo"
    #     self.action_server.start()
    #     #Thread(target=self.update_state).start()



    # COPIED FROM https://github.com/arebgun/dynamixel_motor/blob/master/dynamixel_controllers/src/dynamixel_controllers/joint_trajectory_action_controller.py
    def process_follow_trajectory(self, goal):
        print "1. process_follow_trajectory LORENZO"
        self.process_trajectory(goal.trajectory)

    def process_trajectory(self, traj):
        print "2. process_trajectory LORENZO"
        num_points = len(traj.points)

        # make sure the joints in the goal match the joints of the controller
        delete_me = self.joint_names
        print "hi2"
        if set(self.joint_names) != set(traj.joint_names):
            res = FollowJointTrajectoryResult()
            res.error_code=FollowJointTrajectoryResult.INVALID_JOINTS
            msg = 'Incoming trajectory joints do not match the joints of the controller'
            rospy.logerr(msg)
            rospy.logerr(' self.joint_names={%s}' % (set(self.joint_names)))
            rospy.logerr(' traj.joint_names={%s}' % (set(traj.joint_names)))
            self.action_server.set_aborted(result=res, text=msg)
            return

        # make sure trajectory is not empty
        if num_points == 0:
            msg = 'Incoming trajectory is empty'
            rospy.logerr(msg)
            self.action_server.set_aborted(text=msg)
            return

        # correlate the joints we're commanding to the joints in the message
        # map from an index of joint in the controller to an index in the trajectory
        lookup = [traj.joint_names.index(joint) for joint in self.joint_names]
        durations = [0.0] * num_points

        # find out the duration of each segment in the trajectory
        durations[0] = traj.points[0].time_from_start.to_sec()

        for i in range(1, num_points):
            durations[i] = (traj.points[i].time_from_start - traj.points[i - 1].time_from_start).to_sec()

        if not traj.points[0].positions:
            res = FollowJointTrajectoryResult()
            res.error_code=FollowJointTrajectoryResult.INVALID_GOAL
            msg = 'First point of trajectory has no positions'
            rospy.logerr(msg)
            self.action_server.set_aborted(result=res, text=msg)
            return

        trajectory = []
        time = rospy.Time.now() + rospy.Duration(0.01)

        for i in range(num_points):
            seg = Segment(self.num_joints)

            if traj.header.stamp == rospy.Time(0.0):
                seg.start_time = (time + traj.points[i].time_from_start).to_sec() - durations[i]
            else:
                seg.start_time = (traj.header.stamp + traj.points[i].time_from_start).to_sec() - durations[i]

            seg.duration = durations[i]

            # Checks that the incoming segment has the right number of elements.
            if traj.points[i].velocities and len(traj.points[i].velocities) != self.num_joints:
                res = FollowJointTrajectoryResult()
                res.error_code=FollowJointTrajectoryResult.INVALID_GOAL
                msg = 'Command point %d has %d elements for the velocities' % (i, len(traj.points[i].velocities))
                rospy.logerr(msg)
                self.action_server.set_aborted(result=res, text=msg)
                return

            if len(traj.points[i].positions) != self.num_joints:
                res = FollowJointTrajectoryResult()
                res.error_code=FollowJointTrajectoryResult.INVALID_GOAL
                msg = 'Command point %d has %d elements for the positions' % (i, len(traj.points[i].positions))
                rospy.logerr(msg)
                self.action_server.set_aborted(result=res, text=msg)
                return

            for j in range(self.num_joints):
                if traj.points[i].velocities:
                    seg.velocities[j] = traj.points[i].velocities[lookup[j]]
                if traj.points[i].positions:
                    seg.positions[j] = traj.points[i].positions[lookup[j]]

            trajectory.append(seg)

        rospy.loginfo('Trajectory start requested at %.3lf, waiting...', traj.header.stamp.to_sec())
        rate = rospy.Rate(self.update_rate)

        while traj.header.stamp > time:
            time = rospy.Time.now()
            rate.sleep()

        end_time = traj.header.stamp + rospy.Duration(sum(durations))
        seg_end_times = [rospy.Time.from_sec(trajectory[seg].start_time + durations[seg]) for seg in range(len(trajectory))]

        rospy.loginfo('Trajectory start time is %.3lf, end time is %.3lf, total duration is %.3lf', time.to_sec(), end_time.to_sec(), sum(durations))

        self.trajectory = trajectory
        traj_start_time = rospy.Time.now()

        for seg in range(len(trajectory)):
            rospy.logdebug('current segment is %d time left %f cur time %f' % (seg, durations[seg] - (time.to_sec() - trajectory[seg].start_time), time.to_sec()))
            rospy.logdebug('goal positions are: %s' % str(trajectory[seg].positions))

            # first point in trajectories calculated by OMPL is current position with duration of 0 seconds, skip it
            if durations[seg] == 0:
                rospy.logdebug('skipping segment %d with duration of 0 seconds' % seg)
                continue

            multi_packet = {}

            for port, joints in self.port_to_joints.items():
                vals = []

                for joint in joints:
                    j = self.joint_names.index(joint)

                    start_position = self.joint_states[joint].current_pos
                    if seg != 0: start_position = trajectory[seg - 1].positions[j]

                    desired_position = trajectory[seg].positions[j]
                    desired_velocity = max(self.min_velocity, abs(desired_position - start_position) / durations[seg])

                    self.msg.desired.positions[j] = desired_position
                    self.msg.desired.velocities[j] = desired_velocity

                    # probably need a more elegant way of figuring out if we are dealing with a dual controller
                    if hasattr(self.joint_to_controller[joint], "master_id"):
                        master_id = self.joint_to_controller[joint].master_id
                        slave_id = self.joint_to_controller[joint].slave_id
                        master_pos, slave_pos = self.joint_to_controller[joint].pos_rad_to_raw(desired_position)
                        spd = self.joint_to_controller[joint].spd_rad_to_raw(desired_velocity)
                        vals.append((master_id, master_pos, spd))
                        vals.append((slave_id, slave_pos, spd))
                    else:
                        motor_id = self.joint_to_controller[joint].motor_id
                        pos = self.joint_to_controller[joint].pos_rad_to_raw(desired_position)
                        spd = self.joint_to_controller[joint].spd_rad_to_raw(desired_velocity)
                        vals.append((motor_id, pos, spd))

                multi_packet[port] = vals

            for port, vals in multi_packet.items():
                self.port_to_io[port].set_multi_position_and_speed(vals)

            while time < seg_end_times[seg]:
                # check if new trajectory was received, if so abort current trajectory execution
                # by setting the goal to the current position
                if self.action_server.is_preempt_requested():
                    msg = 'New trajectory received. Aborting old trajectory.'
                    multi_packet = {}

                    for port, joints in self.port_to_joints.items():
                        vals = []

                        for joint in joints:
                            cur_pos = self.joint_states[joint].current_pos

                            motor_id = self.joint_to_controller[joint].motor_id
                            pos = self.joint_to_controller[joint].pos_rad_to_raw(cur_pos)

                            vals.append((motor_id, pos))

                        multi_packet[port] = vals

                    for port, vals in multi_packet.items():
                        self.port_to_io[port].set_multi_position(vals)

                    self.action_server.set_preempted(text=msg)
                    rospy.logwarn(msg)
                    return

                rate.sleep()
                time = rospy.Time.now()

            # Verifies trajectory constraints
            for j, joint in enumerate(self.joint_names):
                if self.trajectory_constraints[j] > 0 and self.msg.error.positions[j] > self.trajectory_constraints[j]:
                    res = FollowJointTrajectoryResult()
                    res.error_code=FollowJointTrajectoryResult.PATH_TOLERANCE_VIOLATED
                    msg = 'Unsatisfied position constraint for %s, trajectory point %d, %f is larger than %f' % \
                           (joint, seg, self.msg.error.positions[j], self.trajectory_constraints[j])
                    rospy.logwarn(msg)
                    self.action_server.set_aborted(result=res, text=msg)
                    return

        # let motors roll for specified amount of time
        rospy.sleep(self.goal_time_constraint)

        for i, j in enumerate(self.joint_names):
            rospy.logdebug('desired pos was %f, actual pos is %f, error is %f' % (trajectory[-1].positions[i], self.joint_states[j].current_pos, self.joint_states[j].current_pos - trajectory[-1].positions[i]))

        # Checks that we have ended inside the goal constraints
        for (joint, pos_error, pos_constraint) in zip(self.joint_names, self.msg.error.positions, self.goal_constraints):
            if pos_constraint > 0 and abs(pos_error) > pos_constraint:
                res = FollowJointTrajectoryResult()
                res.error_code=FollowJointTrajectoryResult.GOAL_TOLERANCE_VIOLATED
                msg = 'Aborting because %s joint wound up outside the goal constraints, %f is larger than %f' % \
                      (joint, pos_error, pos_constraint)
                rospy.logwarn(msg)
                self.action_server.set_aborted(result=res, text=msg)
                break
        else:
	    msg = 'Trajectory execution successfully completed'
	    rospy.loginfo(msg)
	    res = FollowJointTrajectoryResult()
	    res.error_code=FollowJointTrajectoryResult.SUCCESSFUL
            self.action_server.set_succeeded(result=res, text=msg)




    # COPIED FROM https://github.com/arebgun/dynamixel_motor/blob/master/dynamixel_controllers/src/dynamixel_controllers/joint_trajectory_action_controller.py
    ######## END
    ########


'''     FROM FIBONACCI TUTORIAL
    def execute_cb(self, goal):
        print "3. execute_cb LORENZO"
        # helper variables
        r = rospy.Rate(1)
        success = True

        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)

        # publish info to the console for the user
        rospy.loginfo('%s: Executing, creating fibonacci sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))

        # start executing the action
        for i in range(1, goal.order):
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            self._feedback.sequence.append(self._feedback.sequence[i] + self._feedback.sequence[i-1])
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            r.sleep()

        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
'''

if __name__ == '__main__':
    rospy.init_node('braccio_controller')
    server = JointTrajectoryActionController("braccio_controller")
    rospy.spin()
