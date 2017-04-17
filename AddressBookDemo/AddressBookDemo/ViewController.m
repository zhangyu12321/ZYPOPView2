//
//  ViewController.m
//  AddressBookDemo
//
//  Created by MAC15 on 2017/4/11.
//  Copyright © 2017年 MAC15. All rights reserved.
//

#import "ViewController.h"
#import <AddressBook/AddressBook.h>

@interface ViewController ()<UITableViewDelegate,UITableViewDataSource>
@property (nonatomic, strong) NSMutableArray * phoneArray;
@property (nonatomic, strong) NSMutableArray * nameArray;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    self.phoneArray = [[NSMutableArray alloc]init];
    self.nameArray = [[NSMutableArray alloc]init];
    
    [self address];
    
    UITableView * tableview = [[UITableView alloc]initWithFrame:CGRectMake(0, 64, [UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height - 64) style:UITableViewStyleGrouped];
    tableview.delegate = self;
    tableview.dataSource = self;
    [self.view addSubview:tableview];
    
    
}
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section{
    return self.phoneArray.count;
}
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath{
    
    UITableViewCell * cell = [tableView dequeueReusableCellWithIdentifier:@"cellID"];
    if (cell == nil) {
        cell = [[UITableViewCell alloc]initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"cellID"];
    }
    
    NSArray * phonearray = self.phoneArray[indexPath.row];
    
    NSString * phoneNumber = [phonearray componentsJoinedByString:@"/-/"];
    
    cell.textLabel.text = [NSString stringWithFormat:@"%@ ---- %@",self.nameArray[indexPath.row],phoneNumber];
    
    return cell;
}
- (void)address{
    // 1. 判读授权
    ABAuthorizationStatus authorizationStatus = ABAddressBookGetAuthorizationStatus();
    if (authorizationStatus != kABAuthorizationStatusAuthorized) {
        
        NSLog(@"没有授权");
        return;
    }
    
    // 2. 获取所有联系人
    NSMutableArray *phoneArray = [[NSMutableArray alloc]init];

    ABAddressBookRef addressBookRef = ABAddressBookCreate();
    CFArrayRef arrayRef = ABAddressBookCopyArrayOfAllPeople(addressBookRef);
    long count = CFArrayGetCount(arrayRef);
    for (int i = 0; i < count; i++) {
        //获取联系人对象的引用
        ABRecordRef people = CFArrayGetValueAtIndex(arrayRef, i);
        
        //获取当前联系人名字
        NSString *firstName=(__bridge NSString *)(ABRecordCopyValue(people, kABPersonFirstNameProperty));
        
        //获取当前联系人姓氏
        NSString *lastName=(__bridge NSString *)(ABRecordCopyValue(people, kABPersonLastNameProperty));
        NSLog(@"--------------------------------------------------");
        NSLog(@"firstName=%@, lastName=%@", firstName, lastName);
        if (lastName) {
            [self.nameArray addObject:lastName];
            //获取当前联系人的电话 数组
            ABMultiValueRef phones = ABRecordCopyValue(people, kABPersonPhoneProperty);
            for (NSInteger j=0; j<ABMultiValueGetCount(phones); j++) {
                NSString *phone = (__bridge NSString *)(ABMultiValueCopyValueAtIndex(phones, j));
                NSLog(@"phone=%@", phone);
                [phoneArray addObject:phone];
            }
            [self.phoneArray addObject:phoneArray];


        }
        
       
    }
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
