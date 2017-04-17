//
//  ViewController.m
//  CATraneDemo
//
//  Created by MAC15 on 2017/3/17.
//  Copyright © 2017年 MAC15. All rights reserved.
//

#import "ViewController.h"
#define VIEW_HEIGIT 50.0

@interface ViewController ()
@property (nonatomic, strong) UIImageView *one;
@property (nonatomic, strong) UIImageView *two;
@property (nonatomic, strong) UIImageView *three;
@property (nonatomic, strong) UIImageView *four;

@property (nonatomic, strong) UIView *oneShadowView;
@property (nonatomic, strong) UIView *threeShadowView;

@end

@implementation ViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self configFourFoldImage];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark -
#pragma mark - Configuration

- (void)configFourFoldImage
{
    UIView *bgView = [[UIView alloc] initWithFrame:CGRectMake(10, 100, 300, VIEW_HEIGIT*2)];
    [self.view addSubview:bgView];
    
    _one = [[UIImageView alloc] init];
    _one.backgroundColor = [UIColor redColor];
    _one.layer.contentsRect = CGRectMake(0, 0, 1, 0.25);
    _one.layer.anchorPoint = CGPointMake(0.5, 0.0);
    _one.frame = CGRectMake(0, VIEW_HEIGIT, 300, VIEW_HEIGIT);
    
    _two = [[UIImageView alloc] init];
    _two.backgroundColor = [UIColor redColor];
    
    _two.layer.contentsRect = CGRectMake(0, 0.25, 1, 0.25);
    _two.layer.anchorPoint = CGPointMake(0.5, 1.0);
    _two.frame = CGRectMake(0, VIEW_HEIGIT, 300, VIEW_HEIGIT);
    
    _three = [[UIImageView alloc] init];
    _three.backgroundColor = [UIColor redColor];

    
    [bgView addSubview:_two];

    [bgView addSubview:_one];

    
    // 给第一张和第三张添加阴影
    _oneShadowView = [[UIView alloc] initWithFrame:_one.bounds];
    _oneShadowView.backgroundColor = [UIColor blackColor];
    _oneShadowView.alpha = 0.1;
    [_one addSubview:_oneShadowView];
    
    
    [self start];
    
}

#pragma mark -
#pragma mark - Action

- (void)start{
    
    [UIView animateWithDuration:5.0
                          delay:0
         usingSpringWithDamping:1.0
          initialSpringVelocity:0
                        options:UIViewAnimationOptionCurveEaseOut
                     animations:^{
                         
                         // 阴影显示
                         _oneShadowView.alpha = 0;
                         // 折叠
                         _one.layer.transform = [self config3DTransformWithRotateAngle:180.0
                                                                          andPositionY:0];

                     } completion:^(BOOL finished) {
                         
                        
                     }];
}

- (CATransform3D)config3DTransformWithRotateAngle:(double)angle andPositionY:(double)y
{
    CATransform3D transform = CATransform3DIdentity;
    // 立体
    transform.m34 = -1/1000.0;
    // 旋转
    CATransform3D rotateTransform = CATransform3DRotate(transform, M_PI*angle/180, 1, 0, 0);
    // 移动(这里的y坐标是平面移动的的距离,我们要把他转换成3D移动的距离.这是关键,没有它图片就没办法很好地对接。)
    CATransform3D moveTransform = CATransform3DMakeAffineTransform(CGAffineTransformMakeTranslation(0, y));
    // 合并
    CATransform3D concatTransform = CATransform3DConcat(rotateTransform, moveTransform);
    return concatTransform;
}


@end
