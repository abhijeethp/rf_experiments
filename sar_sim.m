clc;clear all;close all;

% Simulate SAR
box = [0 0; 250 250];
rx1_dim = [4 4];
arm_base_dim = [150 100];
arm_length = 80;
rpm = 15;

angle_to_sar = 60;

wavelength = 20;


% animation config
animation_time_s = 4; % time for one rotation
dt_s = 0.1;

% equations
t = 0:dt_s:animation_time_s;
arm_theta_d = rpm * 360 * t / 60;

rx2_x = arm_base_dim(1) + arm_length * cosd(arm_theta_d);
rx2_y = arm_base_dim(2) + arm_length * sind(arm_theta_d);



% plot box
ax1 = nexttile;
hold on;
plot(ax1, [box(1,1) box(2,1)], [box(1,1) box(1,2)], '-k', 'LineWidth', 3);
plot(ax1, [box(1,1) box(1,2)], [box(1,1) box(2,2)], '-k', 'LineWidth', 3);
plot(ax1, [box(1,1) box(2,1)], [box(2,2) box(2,2)], '-k', 'LineWidth', 3);
plot(ax1, [box(2,1) box(2,1)], [box(2,2) box(1,2)], '-k', 'LineWidth', 3);

% plot recievers and arm
arm_base = plot(ax1, arm_base_dim(1), arm_base_dim(2), 'bo','MarkerFaceColor','b', 'MarkerSize',10);
rx1 = plot(ax1, rx1_dim(1), rx1_dim(2), 'ro','MarkerFaceColor','r', 'MarkerSize',12);
rx2 = plot(ax1, rx2_x(1), rx2_y(1), 'ro','MarkerFaceColor','r', 'MarkerSize',12);
arm = plot(ax1, [arm_base_dim(1) rx2_x(1)], [arm_base_dim(2) rx2_y(1)], 'LineWidth',3, 'Color','b');

rx1_rx2_dist = plot(ax1, [rx1_dim(1) rx2_x(1)], [rx1_dim(2) rx2_y(1)], '--');
midpoint = [(rx1_dim(1) + rx2_x(1))/2 (rx1_dim(2) + rx2_y(1))/2];
d = norm(rx1_dim - [rx2_x(1) rx2_y(1)]);
d_label = text(ax1, midpoint(1), midpoint(2), ['d=' num2str(round(d, 2))], 'FontSize',15);

m = (rx2_y(1) - rx1_dim(2))/(rx2_x(1) - rx1_dim(1));
alpha = atand(m);

theta = angle_to_sar - alpha;

xlim = get(gca,'XLim');
x2 = rx1_dim(1)+(240*cosd(theta+alpha));
y2 = rx1_dim(2)+(240*sind(theta+alpha));
rx1_tx = plot([rx1_dim(1) x2],[rx1_dim(2) y2], '--', 'LineWidth',2);

m = (rx1_dim(2) - y2)/(rx1_dim(1) - x2);
a1 = m;
b1 = -1;
c1 = rx1_dim(2) - m * rx1_dim(1);

a2 = -1;
b2 = -1 * m;
c2 = rx2_x(1) + m * rx2_y(1);

x4 = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1);
y4 = (a2 * c1 - a1 * c2) / (a1 * b2 - a2 * b1);
rx2_tx = plot([rx2_x(1) x4],[rx2_y(1) y4], '--', 'LineWidth',2);

midpoint = [(rx1_dim(1) + x4)/2 (rx1_dim(2) + y4)/2];
d_costheta_label = text(midpoint(1), midpoint(2), ['dcos\theta=' num2str(d*cosd(theta))], 'FontSize',15);
disp(['Phase Difference : ' num2str(2 * pi * d * cosd(theta)/ wavelength)]);
% animation

for ii=2:length(arm_theta_d)
    set(rx2, 'XData', rx2_x(ii));
    set(rx2, 'YData', rx2_y(ii));

    set(arm, 'XData', [arm_base_dim(1) rx2_x(ii)]);
    set(arm, 'YData', [arm_base_dim(2) rx2_y(ii)]);

    set(rx1_rx2_dist, 'XData', [rx1_dim(1) rx2_x(ii)]);
    set(rx1_rx2_dist, 'YData', [rx1_dim(2) rx2_y(ii)]);

    midpoint = [(rx1_dim(1) + rx2_x(ii))/2 (rx1_dim(2) + rx2_y(ii))/2];
    d = norm(rx1_dim - [rx2_x(ii) rx2_y(ii)]);
    set(d_label, 'Position', [midpoint(1) midpoint(2) 0]);
    set(d_label, 'String', ['d=' num2str(round(d, 2))]);

    m = (rx2_y(ii) - rx1_dim(2))/(rx2_x(ii) - rx1_dim(1));
    alpha = atand(m);
    theta = angle_to_sar - alpha;

    x2 = rx1_dim(1) + (240 * cosd(theta+alpha));
    y2 = rx1_dim(2) + (240 * sind(theta+alpha));
    set(rx1_tx, 'XData', [rx1_dim(1) x2]);
    set(rx1_tx, 'YData', [rx1_dim(2) y2]);

    
    % reset prependicular    
    m = (rx1_dim(2) - y2)/(rx1_dim(1) - x2);
    a1 = m;
    b1 = -1;
    c1 = rx1_dim(2) - m * rx1_dim(1);
    
    a2 = -1;
    b2 = -1 * m;
    c2 = rx2_x(ii) + m * rx2_y(ii);
    
    x4 = (b1 * c2 - b2 * c1) / (a1 * b2 - a2 * b1);
    y4 = (a2 * c1 - a1 * c2) / (a1 * b2 - a2 * b1);
    set(rx2_tx, 'XData', [rx2_x(ii) x4]);
    set(rx2_tx, 'YData', [rx2_y(ii) y4]);
    
    midpoint = [(rx1_dim(1) + x4)/2 (rx1_dim(2) + y4)/2];
    set(d_costheta_label, 'Position', [midpoint(1) midpoint(2) 0]);
    set(d_costheta_label, 'String', ['dcos\theta=' num2str(d*cosd(theta))]);
    
    drawnow;

    disp(['Phase Difference : ' num2str(2 * pi * d * cosd(theta)/ wavelength)]);
    pause(0.05);
end